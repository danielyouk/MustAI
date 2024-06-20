from dotenv import load_dotenv
import os
import time
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt
import re
import pandas as pd
# Import namespaces
import azure.ai.vision as sdk




def GetTextRead(image_file, outputfile):
    
    load_dotenv()
    ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
    ai_key = os.getenv('AI_SERVICE_KEY')

    # Authenticate Azure AI Vision client
    cv_client = sdk.VisionServiceOptions(ai_endpoint, ai_key)

    analysis_options = sdk.ImageAnalysisOptions()

    features = analysis_options.features = (
        # Specify the features to be retrieved
        sdk.ImageAnalysisFeature.TEXT
    )

    # Get image analysis
    image = sdk.VisionSource(image_file)

    image_analyzer = sdk.ImageAnalyzer(cv_client, image, analysis_options)

    result = image_analyzer.analyze()

    if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:

        # Get image captions
        if result.text is not None:
            # print("\nText:")

            # Prepare image for drawing
            image = Image.open(image_file)
            fig = plt.figure(figsize=(image.width/150, image.height/150))
            plt.axis('off')
            draw = ImageDraw.Draw(image)
            color = 'cyan'
            # Open a text file in write mode
            with open(f'{outputfile}.txt', 'w', encoding='utf-8') as file:
                for line in result.text.lines:
                    # Return the text detected in the image
                    
                    text = line.content
                    drawLinePolygon = True

                    r = line.bounding_polygon
                    bounding_polygon = ((r[0], r[1]),(r[2], r[3]),
                                        (r[4], r[5]),(r[6], r[7])
                                        )
                    # print(f"{text} {bounding_polygon}")  
                    file.write(f"{text} {bounding_polygon}\n")


                    # Draw line bounding polygon                
                    if drawLinePolygon:                    
                        draw.polygon(bounding_polygon, outline=color, width=3)

                    # Draw line bounding polygon                
                    if drawLinePolygon:                    
                        draw.polygon(bounding_polygon, outline=color, width=3)       

            # Save image            
            plt.imshow(image)            
            plt.tight_layout(pad=0)                       
            fig.savefig(outputfile)            
            # print('\n  Results saved')   
            
           

def TexttoTable(textfile):
    with open(textfile, 'r', encoding='utf-8') as file:
        gui_txt = file.read()
    
    # Split the text into lines and then split each line into name and coordinates
    lines = gui_txt.strip().split('\n')

    # Prepare lists to hold the extracted data
    entries = []

    # Process each line to extract the name and the coordinates
    for line in lines:
        # Split line at double "(", then "),"
        name, coords_str = re.split(r'\s+\(\(', line)
        coords_str = coords_str.rstrip(')')
        coords = re.split(r'\), \(', coords_str)

        # Convert string coordinates to tuples of floats
        coords = [tuple(map(float, coord.split(', '))) for coord in coords]
        
        # Append the data as a dictionary to the entries list
        entries.append({'Name': name, 'Coordinates': coords})

    # Create a dataframe from the entries list
    gui_df = pd.DataFrame(entries)

    # Display the dataframe head for brevity
    
    return gui_df