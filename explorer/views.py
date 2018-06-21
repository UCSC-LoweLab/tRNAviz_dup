from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Count
from django.core import serializers
from rest_framework.renderers import JSONRenderer
from collections import defaultdict
from django.http import JsonResponse
import json

import pdb

from . import models
from . import filters
from . import serializers


def summary(request):
  filter_clade = 'Saccharomyces'
  filter_rank = 'genus'
  filter_isotype = 'All'

  clades_qs = models.Consensus.objects.values('clade', 'rank')
  clades = {pair['clade']: pair['rank'] for pair in clades_qs}

  if request.method == "POST":
    filter_clade = request.POST.get('clade')
    filter_rank = clades[filter_clade]
    filter_isotype = request.POST.get('isotype')

  return render(request, 'explorer/summary.html', {
    'clade': filter_clade,
    'rank': filter_rank,
    'isotype': filter_isotype,
    'clades': clades
  })


SINGLE_POSITIONS = [
  '8', '9',
  '14', '15', '16', '17', '17a', '18', '19', '20', '20a', '20b', '21',
  '26',
  '32', '33', '34', '35', '36', '37', '38', 
  '44', '45', '46', '47', '48', 
  'V1', 'V2', 'V3', 'V4', 'V5',
  '54', '55', '56', '57', '58', '59', '60', 
  '73'
]
PAIRED_POSITIONS = [
  '1:72', '2:71', '3:70', '4:69', '5:68', '6:67', '7:66',
  '10:25', '11:24', '12:23', '13:22', 
  '27:43', '28:42', '29:41', '30:40', '31:39', 
  'V11:V21', 'V12:V22', 'V13:V23', 'V14:V24', 'V15:V25', 'V16:V26', 'V17:V27', 
  '49:65', '50:64', '51:63', '52:62', '53:61', 
]

FEATURE_LABELS = {
  'A': 'A', 'G': 'G', 'C': 'C', 'U': 'U', 'Absent': '-',
  'Purine': 'Purine', 'Pyrimidine': 'Pyrimidine',
  'Amino': 'A / C', 'Keto': 'G / U', 'Weak': 'A / U', 'Strong': 'G / C', 
  'B': 'C / G / U', 'H': 'A / C / U', 'D': 'A / G / U', 'V': 'A / C / G', 'N': 'N', 
  'GC': ('G', 'C'), 'AU': ('A', 'U'), 'UA': ('U', 'A'), 'CG': ('C', 'G'), 'GU': ('G', 'U'), 'UG': ('U', 'G'),
  'PurinePyrimidine': ('Purine', 'Pyrimidine'), 'PyrimidinePurine': ('Pyrimidine', 'Purine'), 'WobblePair': ('G / U', 'G / U'),
  'StrongPair': ('G / C', 'G / C'), 'WeakPair': ('A / U', 'A / U'), 'AminoKeto': ('A / C', 'G / U'), 'KetoAmino': ('G / U', 'A / C'),
  'Paired': ('Paired', 'Paired'), 'Bulge': ('Bulge', 'Bulge'), 'Mismatched': ('Mismatched', 'Mismatched'), 'NN': ('N', 'N')
}

SINGLE_FEATURES = ['A', 'C', 'G', 'U']
PAIRED_FEATURES = {
  'AU': 'A:U', 'UA': 'U:A', 'GC': 'G:C', 'CG': 'C:G', 'GU': 'G:U', 'UG': 'U:G', 
  'AA': 'A:A', 'AC': 'A:C', 'AG': 'A:G', 'CA': 'C:A', 'CC': 'C:C', 'CU': 'C:U', 'GA': 'G:A', 'GG': 'G:G', 'UC': 'U:C', 'UU': 'U:U',
  'AM': 'A:-', 'CM': 'C:-', 'GM': 'G:-', 'UM': 'U:-', 'MA': '-:A', 'MC': '-:C', 'MG': '-:G', 'MU': '-:U', 'MM': '-:-'
}

def process_cloverleaf_data_to_json(consensus_qs, freqs_qs):
  plot_data = {}

  # preprocess freqs so Django doesn't submit separate queries per filter
  freqs = {}
  for freq in freqs_qs.values():
    position = freq['position']
    if position in SINGLE_POSITIONS:
      freqs[position] = {base: freq[base] for base in SINGLE_FEATURES}
    elif position in PAIRED_POSITIONS:
      position5, position3 = position.split(':')
      freqs[position5] = {PAIRED_FEATURES[pair]: freq[pair] for pair in PAIRED_FEATURES}
      freqs[position3] = {PAIRED_FEATURES[pair]: freq[pair] for pair in PAIRED_FEATURES}

  consensus = consensus_qs.values()[0]
  for colname in consensus:
    position = colname.replace('p', '').replace('_', ':')
    if position in SINGLE_POSITIONS:
      position_consensus = FEATURE_LABELS[consensus[colname]]
      plot_data[position] = {
        'consensus': position_consensus,
        'freqs': freqs[position]
      }
    if position in PAIRED_POSITIONS:
      position5, position3 = position.split(':')
      plot_data[position5] = {
        'consensus': FEATURE_LABELS[consensus[colname]][0],
        'freqs': freqs[position5]
      }
      plot_data[position3] = {
        'consensus': FEATURE_LABELS[consensus[colname]][1],
        'freqs': freqs[position3]
      }
  return json.dumps(plot_data)

def process_freqs_to_json(clade = 'Saccharomyces'):
  queryset = models.Freq.objects.filter(clade = clade).values('position', 'isotype', 'A', 'G', 'C', 'U', 'absent')
  plot_data = defaultdict(dict)
  for row in queryset:
    plot_data[row['isotype']][row['position']] = {key:row[key] for key in row}
  return plot_data


def get_coords(request):
  data = models.Coord.objects.all()
  serializer = serializers.CoordSerializer(data, many = True)
  return JsonResponse(serializer.data, safe = False)

def cloverleaf(request, clade, isotype):
  consensus_qs = models.Consensus.objects.filter(clade = clade, isotype = isotype)
  freqs_qs = models.Freq.objects.filter(clade = clade, isotype = isotype)
  return JsonResponse(process_cloverleaf_data_to_json(consensus_qs, freqs_qs), safe = False)
