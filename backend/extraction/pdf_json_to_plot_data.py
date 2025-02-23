import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def generate_plot_values_from_provided_data(input_json):
    def extract_plot_ideas(json_data):
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
            You are a highly skilled accountant and finance/tax expert who specializes in reporting taxes with clear, 
            insightful visualizations that simplify the process for both you and your clients. You are working with tax 
            and finance data in JSON format. Using this data, generate the most effective and valuable visualizations that 
             can be pitched to the client. The more useful and insightful the visualization, the more brownie points you earn. 
            If the client approves a visualization, you get a brownie point—better visualizations earn more points.

            #plot types to generate: Pie Chart, Bar Chart, Line Chart, Scatter Plot, Heatmap
            parameters to use for pie chart:
             - data: the data to be plotted
             - names: the names of the data
             - title: the title of the plot
             - labels: the labels of the plot
             - colors: the colors of the plot
             - legend: the legend of

            parameters to use for the bar chart:
             - x axis: the categories of the data
             - height: the corresponding values of the data
             - title: the title of the plot
             - labels: the labels of the plot
             - colors: the colors of the plot
             - legend: the legend of the plot
             - width: the width of the plot
             - axis: horizontal or vertical
             
            parameters to use for the line chart:
             - x axis: the categories/type of the data
             - y axis: the corresponding values of the data
             - names: the names of the data
             - title: the title of the plot
             - labels: the labels of the plot
             - colors: the colors of the plot
             - legend: the legend of the plot
            
            parameters to use for the scatter plot:
             - x axis: the independent data
             - y axis: the dependent data
             - title: the title of the plot
             - labels: the labels of the plot
             - colors: the colors of the plot
             - legend: the legend of the plot
            
            parameters to use for the heatmap:
             - data: the data to be plotted
             - vmin : the minimum value of the plot to anchor the color scale
             - vmax : the maximum value of the plot to anchor the color scale
             - names: the names of the data
             - title: the title of the plot
             - labels: the labels of the plot
             - colors: the colors of the plot
             - legend: the legend of the plot

            Give me a dictionary of the best visualizations that I can use to pitch to my client and how it will be useful to them.
            The output MUST follow the following rules: 
            
            # NO VALUES, ALL THE DATA MUST BE TEXT DESCRBING THE VALUES CORRESPONDING TO THAT PARAMETER
            # ONLY PRODUCE 3-5 MEANINGFUL GRAPHS, NO MORE, NO LESS. 
            # MAKE SURE TO PRODUCE ONLY DISCTINCT GRAPHS, NO DUPLICATES, AND BE MORE DESCRIPTIVE
            # do not return any extra information, just the json format information
             
            DONT GIVE MORE THAN 5 GRAPHS
            DONT GIVE LESS THAN 4 GRAPHS
            DO NOT HAVE ANY DUPLICATE GRAPHS
            DO NOT HAVE ANY DUPLICATE GRAPHS
            
            
            Please follow this format STRICTLY
            {
            "graph_name_1": {"type": "*type of graph 1*", "description": "*description of graph 1*", parameters: {"parameter_1": "value_type_1", "parameter_2": "value_type_2", ...}},
            "graph_name_2": {.......}
            } """
            },
            {
                "role": "user",
                "content": str(json_data)
            }
        ]
        )
        output = completion.choices[0].message.content
        try:
            # Remove any markdown formatting if present
            if "```json" in output:
                output = output.split("```json")[1].split("```")[0]
            elif "```" in output:
                output = output.split("```")[1]
                
            # Clean up the output and parse JSON
            output = output.strip()
            return json.loads(output)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return {}
    
    def extract_plot_values(plot_json, total_info_json):
        full_data = {}
        for plot in plot_json.keys(): 
            completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                "content":
                """
                You are the smartest, most descriptive, accountant cum finance/tax expert who specializes in reporting a person's taxes through them 
                with the aid of visualizations that make your and your client's lives easier. You are now working with data in a json format. Using the data,
                do what you do best and think of all potential viable visualizations that I can pitch to my client. You love brownie points
                and if you the client approves of the visualization, you get a brownie point. The better the visualization, the more brownie points you get.
                The data will pertain to everything finance and tax related. Make sure to extract the EXACT DATA that you need from the json format 

                #plot types to generate: Pie Chart, Bar Chart, Line Chart, Scatter Plot, Heatmap
                parameters to use for pie chart:
                - data: the data to be plotted
                - names: the names of the data
                - title: the title of the plot
                - labels: the labels of the plot
                - colors: the colors of the plot
                - legend: the legend of

                parameters to use for the bar chart:
                - x axis: the categories of the data
                - height: the corresponding values of the data
                - title: the title of the plot
                - labels: the labels of the plot
                - colors: the colors of the plot
                - legend: the legend of the plot
                - width: the width of the plot
                - axis: horizontal or vertical
                
                parameters to use for the line chart:
                - x axis: the categories/type of the data
                - y axis: the corresponding values of the data
                - names: the names of the data
                - title: the title of the plot
                - labels: the labels of the plot
                - colors: the colors of the plot
                - legend: the legend of the plot
                
                parameters to use for the scatter plot:
                - x axis: the independent data
                - y axis: the dependent data
                - title: the title of the plot
                - labels: the labels of the plot
                - colors: the colors of the plot
                - legend: the legend of the plot
                
                parameters to use for the heatmap:
                - data: the data to be plotted
                - vmin : the minimum value of the plot to anchor the color scale
                - vmax : the maximum value of the plot to anchor the color scale
                - names: the names of the data
                - title: the title of the plot
                - labels: the labels of the plot
                - colors: the colors of the plot
                - legend: the legend of the plot


                Give me a dictionary of the best visualizations that I can use to pitch to my client and how it will be useful to them. The output MUST be in 
                the following format: 
                
                ## emphasis on this point - for the parameters, make sure that the parameters are the actual values (say in a scatterplot, the actual numerical x and y values to be
                used in the plot) similar for other graphs
                # do not return any extra information, just the json format information
                
                Please follow this format STRICTLY
                {
                "graph_name_1": {"type": "*type of graph 1*", "description": "*description of graph 1*", parameters: {"parameter_1": "value_type_1", "parameter_2": "value_type_2", ...}}
                } 
                """
                },
                {
                    "role": "user",
                    "content": f'plot name: {plot}. Data to be extracted from: {str(total_info_json)}'
                }
            ]
        )
            output = completion.choices[0].message.content
            try:
                json_str = output[output.find('{'):output.rfind('}')+1]  # Extract JSON part
                full_data[plot] = json.loads(json_str)
            except json.JSONDecodeError:
                full_data[plot] = {"error": "Failed to parse response"}
        
        return full_data
    

    
    plot_ideas = extract_plot_ideas(input_json)
    return extract_plot_values(plot_json=plot_ideas, total_info_json=input_json)