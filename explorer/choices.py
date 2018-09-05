from . import models

CLADES = tuple([(clade.taxid, '{} ({})'.format(clade.name, clade.rank)) for clade in models.Taxonomy.objects.order_by('name')])

ISOTYPES = (
  ('All', 'All isotypes'),
  ('Ala', 'Ala'),
  ('Arg', 'Arg'),
  ('Asn', 'Asn'),
  ('Asp', 'Asp'),
  ('Cys', 'Cys'),
  ('Gln', 'Gln'),
  ('Glu', 'Glu'),
  ('Gly', 'Gly'),
  ('His', 'His'),
  ('Ile', 'Ile'),
  ('iMet', 'iMet'),
  ('Leu', 'Leu'),
  ('Lys', 'Lys'),
  ('Met', 'Met'),
  ('Phe', 'Phe'),
  ('Pro', 'Pro'),
  ('Ser', 'Ser'),
  ('SeC', 'SeC'),
  ('Thr', 'Thr'),
  ('Trp', 'Trp'),
  ('Tyr', 'Tyr'),
  ('Val', 'Val'),
)

SINGLE_POSITIONS = (
  ('single', 'Single positions'),
  ('p8', '8'),
  ('p9', '9'),
  ('p14', '14'),
  ('p15', '15'),
  ('p16', '16'),
  ('p17', '17'),
  ('p17a', '17a'),
  ('p18', '18'),
  ('p19', '19'),
  ('p20', '20'),
  ('p20a', '20a'),
  ('p20b', '20b'),
  ('p21', '21'),
  ('p26', '26'),
  ('p32', '32'),
  ('p33', '33'),
  ('p34', '34'),
  ('p35', '35'),
  ('p36', '36'),
  ('p37', '37'),
  ('p38', '38'),
  ('p44', '44'),
  ('p45', '45'),
  ('p46', '46'),
  ('p47', '47'),
  ('p48', '48'),
  ('p54', '54'),
  ('p55', '55'),
  ('p56', '56'),
  ('p57', '57'),
  ('p58', '58'),
  ('p59', '59'),
  ('p60', '60'),
  ('p73', '73'),
)

PAIRED_POSITIONS = (
  ('paired', 'Paired positions'),
  ('p1_72', '1:72'),
  ('p2_71', '2:71'),
  ('p3_70', '3:70'),
  ('p4_69', '4:69'),
  ('p5_68', '5:68'),
  ('p6_67', '6:67'),
  ('p7_66', '7:66'),
  ('p10_25', '10:25'),
  ('p11_24', '11:24'),
  ('p12_23', '12:23'),
  ('p13_22', '13:22'),
  ('p27_43', '27:43'),
  ('p28_42', '28:42'),
  ('p29_41', '29:41'),
  ('p30_40', '30:40'),
  ('p31_39', '31:39'),
  ('p49_65', '49:65'),
  ('p50_64', '50:64'),
  ('p51_63', '51:63'),
  ('p52_62', '52:62'),
  ('p53_61', '53:61'),
)

VARIABLE_LOOP_POSITIONS = (
  ('variable', 'Variable arm'),
  ('pV1', 'V1'),
  ('pV2', 'V2'),
  ('pV3', 'V3'),
  ('pV4', 'V4'),
  ('pV5', 'V5'),
  ('pV11_V21', 'V11:V21'),
  ('pV12_V22', 'V12:V22'),
  ('pV13_V23', 'V13:V23'),
  ('pV14_V24', 'V14:V24'),
  ('pV15_V25', 'V15:V25'),
  ('pV16_V26', 'V16:V26'),
  ('pV17_V27', 'V17:V27'),
)

TERTIARY_INTERACTIONS = (
  ('tertiary', 'Tertiary interactions'),
  ('p8_14', '8:14'),
  ('p9_23', '9:23'),
  ('p10_45', '10:45'),
  ('p15_48', '15:48'),
  ('p18_55', '18:55'),
  ('p19_56', '19:56'),
  ('p22_46', '22:46'),
  ('p26_44', '26:44'),
  ('p54_58', '54:58'),
)

POSITIONS = SINGLE_POSITIONS + PAIRED_POSITIONS + VARIABLE_LOOP_POSITIONS + TERTIARY_INTERACTIONS