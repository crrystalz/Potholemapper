import os
import shutil

import cv2
import base64

from dash import Dash, dcc, html, Input, Output, State, callback
from dash.exceptions import PreventUpdate

from test_script import test

from main import main

app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-video",
            children=html.Div(["Drag and Drop or ", html.A("Select .mp4")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        dcc.Upload(
            id="upload-gpx",
            children=html.Div(["Drag and Drop or ", html.A("Select .gpx")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=False,
        ),
        html.Div(id="output-video-upload"),
    ]
)


@callback(
    Output("output-video-upload", "children"),
    Input("upload-video", "contents"),
    Input("upload-gpx", "contents"),
)
def uploaded(video_contents, gpx_contents):
    if video_contents is None or gpx_contents is None:
        raise PreventUpdate

    else:
        video_type, video_string = video_contents.split(",")
        gpx_type, gpx_string = gpx_contents.split(",")

        with open("uploaded.mp4", "wb") as f:
            f.write(base64.b64decode(video_string))

        with open("uploaded.gpx", "wb") as f:
            f.write(base64.b64decode(gpx_string))


        # os.system(
        # 'mapillary_tools video_process uploaded.mp4 --geotag_source "gpx" --geotag_source_path uploaded.gpx --interpolation_use_gpx_start_time --video_sample_distance -1 --video_sample_interval 2'
        # )

        # image_raw_dir = "mapillary_sampled_video_frames/uploaded.mp4"
        # image_geotagged_dir = "confirmed_geotagged_images/"
        # output_dir = "yolo_output/"
        # model_path = "../detection_model/yolov8x_tesladataset1.pt"

        # os.mkdir(image_geotagged_dir)
        # os.mkdir(output_dir)

        # main(image_raw_dir, image_geotagged_dir, output_dir, model_path)


if __name__ == "__main__":
    app.run(debug=True)
