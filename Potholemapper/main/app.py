from dash import Dash, dcc, html, Input, Output, State, callback

import cv2

source_dir = f"../testing/images/"
output_dir = f"../testing/yolo_output/"

model_name = f"yolov8x_tesladataset1.pt"
model_path = f"../detection_model/{model_name}"

app = Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-data-upload')
])


@callback(
    Output('output-data-upload', 'children'),
    Input('upload-image', 'contents')
)


def uploaded(contents):
    if 
    print(type(contents))
    # capture = cv2.VideoCapture(contents)
    # frameNr = 0
 
    # while (True):
    
    #     success, frame = capture.read()
    
    #     if success:
    #         cv2.imwrite(f"../testing/app/images/_{frameNr}.jpg", frame)
    
    #     else:
    #         break
    
    #     frameNr = frameNr+1

    #     y="r"
    
    # capture.release()

    return y


if __name__ == '__main__':
    app.run(debug=True)
