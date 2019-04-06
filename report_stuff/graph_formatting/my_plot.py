def set_size(width, fraction=1, subplot=[1, 1]):
	# Width of figure
	fig_width_pt = width * fraction

	# Convert from pt to inches
	inches_per_pt = 1 / 72.27

	# Golden ratio to set aesthetic figure height
	golden_ratio = (5**.5 - 1) / 2

	# Figure width in inches
	fig_width_in = fig_width_pt * inches_per_pt
	# Figure height in inches
	fig_height_in = fig_width_in * golden_ratio * (subplot[0] / subplot[1])

	fig_dim = (fig_width_in, fig_height_in)

	return fig_dim
