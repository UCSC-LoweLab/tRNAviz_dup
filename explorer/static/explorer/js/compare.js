var bitchart_data;
var all_features = ['A', 'C', 'G', 'U', '-', 'A:U', 'U:A', 'G:C', 'C:G', 'G:U', 'U:G', 'A:A', 'A:C', 'A:G', 'C:A', 'C:C', 'C:U', 'G:A', 'G:G', 'U:C', 'U:U', '-:A', '-:C', '-:G', '-:U']
var sorted_positions = ['1:72', '2:71', '3:70', '4:69', '5:68', '6:67', '7:66', '8', '9', '10:25', '11:24', '12:23', '13:22', '14', '15', '16', '17', '17a', '18', '19', '20', '20a', '20b', '21', '26', '27:43', '28:42', '29:41', '30:40', '31:39', '32', '33', '34', '35', '36', '37', '38', '44', '45', '46', '47', '48', '49:65', '50:64', '51:63', '52:62', '53:61', '54', '55', '56', '57', '58', '59', '60', '73']
var groups;
var adata;
var group_scale, position_scale, score_scale;
var draw_bitchart = function(plot_data) {
	bitchart_data = JSON.parse(plot_data);
	bits = Object.values(bitchart_data['bits']);
	groups = bitchart_data['groups']

  d3.select('#plot-area .loading-overlay').style('display', 'none');

	var plot_width = sorted_positions.length * 40,
			plot_height = groups.length * 40,
			plot_margin = 100,
			tile_width = 30;
	
	var y_axis_offset = 7 * groups.reduce(function (a, b) { return a.length > b.length ? a : b; }).length;

	var svg = d3.select('#plot-area')
		.append('svg')
		.attr('id', 'plot-svg')
		.attr('width', plot_width + plot_margin)
		.attr('height', plot_height + plot_margin)
	
	var bitchart = svg.append('g')
		.attr('id', 'bitchart-plot')

	var position_scale = d3.scaleBand()
		.domain(sorted_positions)
		.range([0, sorted_positions.length * 35])
		.padding(0.1);

  var position_axis = d3.axisBottom(position_scale);

  group_scale = d3.scaleBand()
    .domain(groups)
    .range([0, groups.length * 35])
    .padding(0.1);

  var group_axis = d3.axisLeft(group_scale);

  var score_scale = d3.scaleLinear()
    .domain([-15, -5, 0])
    .range(['#5d478b', '#b22222', 'white'])

  var alpha_scale = d3.scaleLinear()
  	.domain([-15, -5, 0])
  	.range([1, 1, 0.4])


  bitchart.append('g')
    .attr('class', 'xaxis')
    .attr('transform', 'translate(' + y_axis_offset + ', ' + groups.length * 35 + ')')
    .call(position_axis);

  bitchart.append('g')
    .attr('class', 'yaxis')
    .attr('transform', 'translate(' + y_axis_offset + ', 0)')
    .call(group_axis);

  bitchart.selectAll('.xaxis text')
    .attr('class', 'axis-text')
    .attr('text-anchor', 'end')
    .attr('transform', function(d) { return 'translate(-' + this.getBBox().height + ', ' + (this.getBBox().height) + ') rotate(-90)'; });

  bitchart.selectAll('.yaxis text')
    .attr('class', 'axis-text')
    .attr('id', d => 'tick-' + sorted_positions[d]);

  var tiles = bitchart.selectAll('.groups')
  	.data(bits)
  	.enter()
  	.append('g')
  	.attr('class', 'tile')

  tiles.append('rect')
  	.attr('id', d => 'tile-' + d['position'] + '-' + escape(d['seqname']))
  	.attr('class', 'bitchart-tile')
  	.attr('transform', 'translate(' + y_axis_offset + ', 0)')
  	.attr('x', d => position_scale(d['position']))
  	.attr('y', d => group_scale(d['seqname']))
  	.attr('width', tile_width)
  	.attr('height', tile_width)
  	.style('fill', d => score_scale(d['score']))
  	.style('fill-opacity', d => alpha_scale(d['score']))

  tiles.append('text')
  	.attr('id', d => 'annot-' + d['position'] + '-' + escape(d['seqname']))
  	.attr('class', 'bitchart-annot')
  	.attr('transform', 'translate(' + y_axis_offset + ', 0)')
    .attr('text-anchor', 'middle')
    .attr('alignment-baseline', 'middle')
    .attr('font-size', '0.8em')
  	.attr('x', d => position_scale(d['position']) + tile_width / 2)
  	.attr('y', d => group_scale(d['seqname']) + tile_width / 2)
  	.text(d => d['feature'])
  	.style('fill', d => (d['score'] < -4) ? 'white' : 'black')

};
