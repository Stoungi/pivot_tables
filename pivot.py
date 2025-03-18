from Process import Process


file = Process('large_pivot_table_data.xlsx')



file.input(**{"Region" : ["North"], "Chart" : ["bar", "line", "pie"], "save as": "just_north.pdf"})

file.input(**{"Region" : ["North", "East"], "Chart" : "*", "save as": "north_vs_west.pdf"})

file.input()
