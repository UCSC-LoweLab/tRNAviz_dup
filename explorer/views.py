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
  filter_info = {
    'clade': 'Saccharomyces',
    'rank': 'genus',
    'isotypes': 'All'
  }
  consensus_qs = models.Consensus.objects.filter(clade = 'Saccharomyces', isotype = 'All')
  plot_data = {}
  plot_data['cloverleaf'] = process_cloverleaf_data_to_json(consensus_qs)
  # plot_data['freqs'] = serializers.serialize("json", models.Freq.objects.filter(clade = 'Saccharomyces', isotype = 'All'))
  plot_data['freqs'] = process_freqs_to_json()
  return render(request, 'explorer/summary.html', {
    'filter_info': filter_info,
    'plot_data': plot_data,
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

def process_cloverleaf_data_to_json(queryset):
  plot_data = {}
  consensus = queryset.values()[0] 
  for colname in consensus:
    position = colname.replace('p', '').replace('_', ':')
    if position in SINGLE_POSITIONS:
      plot_data[position] = FEATURE_LABELS[consensus[colname]]
    if position in PAIRED_POSITIONS:
      position5, position3 = position.split(':')
      plot_data[position5], plot_data[position3] = FEATURE_LABELS[consensus[colname]]
  
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

def cloverleaf(request):
  consensus_qs = models.Consensus.objects.filter(clade = 'Saccharomyces', isotype = 'All')
  return JsonResponse(process_cloverleaf_data_to_json(consensus_qs), safe = False)