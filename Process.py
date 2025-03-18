import pandas as pd
import matplotlib.pyplot as plt
from Report import Report
from Generator import Generator
from typing import List, Dict, Any

# opens  the spreadsheet to process the data
class Process:
    def __init__(self, file_path):
        """
        Initializes the Process class with the Excel file path.
        """
        self.file_path = file_path

    def input(self, **criteria: Dict[str, Any]):
        """
        Handles the user input for regions, categories, months, and chart types.
        """

        default_values = {
            "Region": ["North", "South", "West", "East"],
            "Category": ["Furniture", "Electronics", "Clothing", "Books"],
            "Chart": ['bar', 'pie', 'heatmap', 'line'],
            "Month": [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]
        }

        # Get user regions, default to * if not provided or empty
        user_regions = criteria.get("Region", "*")
        if user_regions == "*" or not user_regions:
            user_regions = default_values["Region"]

        # Get user categories, default to * if not provided or empty
        user_categories = criteria.get("Category", "*")
        if user_categories == "*" or not user_categories:
            user_categories = default_values["Category"]

        # Get chart types, default to * if not provided or empty
        chart_types = criteria.get("Chart", "*")
        if chart_types == "*" or not chart_types:
            chart_types = default_values["Chart"]
        try:
            if len(criteria["Region"]) == 1:
                    chart_types.remove("pie")
        except:
                pass

        # Get month(s), default to * if not provided or empty
        month = criteria.get("Month", "*")
        if month == "*" or not month:
            month = default_values["Month"]

        save_as = criteria.get("save as")
        if not save_as:
            save_as = "sales_comparison_report.pdf"
        # Call the run method with the processed inputs
        self.run(user_regions, user_categories, chart_types, month, save_as)

    def process_data(self, user_regions, user_categories, month):
        """
        Processes the data based on user input and returns the filtered comparison data.
        """
        # Read the data from the Excel file
        data = pd.read_excel(self.file_path, sheet_name='Data')

        # Filter by region if user input is provided
        if user_regions:
            data = data[data['Region'].isin(user_regions)]

        # Filter by month if user input is provided
        data = data[data['Month'].isin(month)]

        # Group the data by Region, Month, and Category, and sum the sales
        comparison_data = (
            data.groupby(['Region', 'Month', 'Category'])['Sales']
            .sum()
            .reset_index()
        )

        # Ensure months appear in correct order
        comparison_data['Month'] = pd.Categorical(comparison_data['Month'], categories=month, ordered=True)
        comparison_data = comparison_data.sort_values('Month')

        # Define color palette for the regions (for consistency across all charts)
        regions = comparison_data['Region'].unique()
        colors = plt.cm.Paired.colors  # Use a colormap for distinct colors (up to 10 regions)
        region_color_map = {region: colors[i % len(colors)] for i, region in enumerate(regions)}

        return comparison_data, region_color_map

    def run(self, user_regions, user_categories, chart_types, month, save_as='sales_comparison_report.pdf'):
        """
        Runs the entire process: gets user input, processes data, and generates the report.
        """


        # Process data
        comparison_data, region_color_map = self.process_data(user_regions, user_categories, month)

        # Create report and generator objects, passing months_order to Generator
        report = Report(save_as)
        generator = Generator(comparison_data, month, region_color_map, month)
        print("Please wait...")

        # Generate report
        for category in user_categories or comparison_data['Category'].unique():
            report.save_report(generator, category, chart_types)

        # Close the report
        report.close()
