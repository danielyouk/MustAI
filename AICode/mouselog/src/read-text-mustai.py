from dotenv import load_dotenv
import os
import time
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces
import azure.ai.vision as sdk


def main():

    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Authenticate Azure AI Vision client
        cv_client = sdk.VisionServiceOptions(ai_endpoint, ai_key)


        # Menu for text reading functions
        print('\nUse Read API for image text reading\n')
        path = input('Enter the path to the image file to read text from:')
        
        image_file = os.path.join('..','images',path)
        GetTextRead(image_file)
        
                

    except Exception as ex:
        print(ex)

def GetTextRead(image_file):
    print('\n')

    # Use Analyze image function to read text in image

    print('Reading text in {}\n'.format(image_file))

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
            print("\nText:")

            # Prepare image for drawing
            image = Image.open(image_file)
            fig = plt.figure(figsize=(image.width/100, image.height/100))
            plt.axis('off')
            draw = ImageDraw.Draw(image)
            color = 'cyan'
            # Open a text file in write mode
            with open('../output/static-structural-gui.txt', 'w', encoding='utf-8') as file:
                for line in result.text.lines:
                    # Return the text detected in the image
                    
                    text = line.content
                    drawLinePolygon = True

                    r = line.bounding_polygon
                    bounding_polygon = ((r[0], r[1]),(r[2], r[3]),
                                        (r[4], r[5]),(r[6], r[7])
                                        )
                    print(f"{text} {bounding_polygon}")  
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
            outputfile = '../output/static-structural-gui.jpg'            
            fig.savefig(outputfile)            
            print('\n  Results saved in', outputfile)   




if __name__ == "__main__":
    main()
