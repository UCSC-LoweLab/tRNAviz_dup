from . import models

class DAGNode(object):
  def __init__(self, tax, parent):
    self.tax = tax
    self.parent = parent
    self.children = []

  def addChild(self, child):
    self.children.append(child)

  def isParentOf(self, node):
    return node.tax in [child.tax for child in self.children]

  def indexOfChild(self, tax):
    return([child.tax for child in self.children].index(tax))

  def __eq__(self, other):
    return self.tax == other.tax

  def __ne__(self, other):
    return self.tax != other.tax

  def __str__(self):
    children = ', '.join([str(child.tax) for child in self.children])
    if type(self.tax) == str: # root
      return('root -> [{}]'.format(children))
    return('{} -> [{}]'.format(self.tax, children))

  def getAllChildrenAsString(self, output = ''):
    ''' Return all children '''
    if len(self.children) > 0:
      children = []
      for child in self.children:
        children.append(child.getAllChildrenAsString(output))
      if len(children) > 0:
        return '{}\n{}'.format(self.tax, '\n'.join(children))
    return str(self.tax)

  def makeIterable(self):
    ''' Django template is clunky with recursion - pass generator that yields the correct values instead '''
    if len(self.children) != 0:
      yield {'start_nodes': True, 'data': self}
      for child in self.children:
        yield {'start_node': True, 'data': child}
        for i in child.makeIterable():
          yield i
        yield {'end_node': True}
      yield {'end_nodes': True}

class Tree(object):
  ''' Convert Taxonomy model into a tree '''
  def __init__(self):
    self.root = DAGNode('root', 'root')
    assembly_qs = models.Taxonomy.objects.filter(rank = 'assembly')
    # Iterate through assemblies and connect each to the main tree
    ranks = ['assembly', 'species', 'genus', 'family', 'order', 'subclass', 'taxclass', 'subphylum', 'phylum', 'subkingdom', 'kingdom', 'domain']
    for assembly_tax in assembly_qs:
      parent = self.root
      tax_qs = models.Taxonomy.objects.filter(taxid__in = [getattr(assembly_tax, rank) for rank in ranks])
      for tax in sorted(tax_qs, key = lambda x: -ranks.index(x.rank if x.rank != 'class' else 'taxclass')):
        current_node = DAGNode(tax, parent)
        if parent.isParentOf(current_node):
          parent = parent.children[parent.children.index(current_node)]
        else:
          parent.addChild(current_node)
          parent = current_node