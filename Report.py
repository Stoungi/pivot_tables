from matplotlib.backends.backend_pdf import PdfPages
# the chosen representations from the main program are applied
class Report:
    def __init__(self, pdf_path):
        """
        Initializes the Report class with the path where the PDF will be saved.
        """
        self.pdf_path = pdf_path
        self.pdf_pages = PdfPages(pdf_path)

    def save_report(self, generator, category, chart_types):
        """
        Saves the generated charts into a PDF.
        """
        if 'bar' in chart_types:
            generator.generate_bar_chart(category, self.pdf_pages)
        if 'pie' in chart_types:
            generator.generate_pie_charts(category, self.pdf_pages)
        if 'heatmap' in chart_types:
            generator.generate_heatmap(category, self.pdf_pages)
        if 'line' in chart_types:
            generator.generate_line_graph(category, self.pdf_pages)

    def close(self):
        """
        Closes the PDF after all charts have been saved.
        """
        self.pdf_pages.close()
        print(f"All charts saved to {self.pdf_path}")
