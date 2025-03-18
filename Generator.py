import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# generates the pdf file



class Generator:
    def __init__(self, comparison_data, months_order, region_color_map, user_months):
        """
        Initializes the Generator class with the data needed for chart generation.
        """
        self.comparison_data = comparison_data
        self.months_order = months_order
        self.region_color_map = region_color_map
        self.user_months = user_months  # Store user-selected months

    def generate_bar_chart(self, category, pdf_pages):
        """
        Generates a bar chart for the given category and saves it to the PDF.
        """
        category_data = self.comparison_data[self.comparison_data['Category'] == category]

        # Filter category data based on selected months
        category_data = category_data[category_data['Month'].isin(self.user_months)]

        plt.figure(figsize=(14, 8))
        x = np.arange(len(self.user_months))  # Month positions on x-axis
        bar_width = 0.15  # Width of each bar for better spacing

        # Loop through each region to plot sales data
        for i, region in enumerate(category_data['Region'].unique()):
            subset = category_data[category_data['Region'] == region]
            sales = [subset[subset['Month'] == month]['Sales'].sum() for month in self.user_months]
            plt.bar(
                x + i * bar_width, sales, width=bar_width,
                label=f"{region}", color=self.region_color_map[region]
            )

        plt.xticks(x + bar_width * len(category_data['Region'].unique()) / 2, self.user_months, rotation=45)
        plt.title(f'Monthly Sales Comparison for {category} by Region', fontsize=16)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save to the PDF
        pdf_pages.savefig()
        plt.close()

    def generate_pie_charts(self, category, pdf_pages):
        """
        Generates pie charts for each month for the given category and saves it to the PDF.
        """
        category_data = self.comparison_data[self.comparison_data['Category'] == category]
        # Filter category data based on selected months
        category_data = category_data[category_data['Month'].isin(self.user_months)]

        fig, axes = plt.subplots(3, 4, figsize=(18, 12))  # 3x4 grid for 12 months
        axes = axes.flatten()

        for i, month in enumerate(self.user_months):
            month_data = category_data[category_data['Month'] == month]
            region_sales = month_data.groupby('Region')['Sales'].sum()
            ax = axes[i]
            ax.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%',
                   colors=[self.region_color_map[region] for region in region_sales.index],
                   startangle=90, wedgeprops={'edgecolor': 'black'})
            ax.set_title(f"{month}", fontsize=12)

        plt.suptitle(f"Sales Distribution by Region for {category} (Pie Charts by Month)", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to fit the title
        pdf_pages.savefig()
        plt.close()

    def generate_heatmap(self, category, pdf_pages):
        """
        Generates a heatmap for the given category and saves it to the PDF.
        """
        category_data = self.comparison_data[self.comparison_data['Category'] == category]
        # Filter category data based on selected months
        category_data = category_data[category_data['Month'].isin(self.user_months)]

        pivot_data = category_data.pivot_table(index='Region', columns='Month', values='Sales', aggfunc='sum', observed=False)

        plt.figure(figsize=(12, 8))
        sns.heatmap(
            pivot_data, annot=True, cmap='YlGnBu', fmt='.1f', cbar_kws={'label': 'Total Sales ($)'},
            linewidths=0.5, linecolor='gray', xticklabels=self.user_months,  # Use user-selected months here
            yticklabels=category_data['Region'].unique()
        )

        plt.title(f"Heatmap of Sales by Region and Month for {category}", fontsize=16)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Region', fontsize=12)
        plt.tight_layout()
        pdf_pages.savefig()
        plt.close()

    def generate_line_graph(self, category, pdf_pages):
        """
        Generates a line graph to show the sales trend by month for each region and saves it to the PDF.
        """
        category_data = self.comparison_data[self.comparison_data['Category'] == category]

        # Filter category data based on selected months
        category_data = category_data[category_data['Month'].isin(self.user_months)]

        # Create a new figure
        plt.figure(figsize=(14, 8))

        # Loop through each region to plot the line graph
        for region in category_data['Region'].unique():
            subset = category_data[category_data['Region'] == region]
            sales = [subset[subset['Month'] == month]['Sales'].sum() for month in self.user_months]

            # Plot the line graph for each region
            plt.plot(self.user_months, sales, label=f"{region}", marker='o', color=self.region_color_map[region])

        plt.title(f'Sales Trend for {category} by Region', fontsize=16)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Total Sales ($)', fontsize=12)
        plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Save to the PDF
        pdf_pages.savefig()
        plt.close()

