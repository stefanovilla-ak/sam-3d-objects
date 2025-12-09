import os
import sys
import argparse
import imageio

# import inference code
sys.path.append("notebook")
from inference import Inference, load_image, load_single_mask, load_mask
from inference import ready_gaussian_for_video_rendering, render_video, display_image, make_scene, interactive_visualizer
from IPython.display import Image as ImageDisplay
#%%



def main(image, mask, output_folder=None):
    PATH = os.getcwd()
    TAG = "hf"
    config_path = f"{PATH}/../checkpoints/{TAG}/pipeline.yaml"

    IMAGE_NAME = os.path.basename(os.path.dirname(image))

    image = load_image(image)
    mask = load_mask(mask)

    output_folder = output_folder if output_folder else os.path.join(PATH, "output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # load model
    tag = "hf"
    config_path = f"checkpoints/{tag}/pipeline.yaml"
    inference = Inference(config_path, compile=False)

    # run model
    _output = inference(image, mask, seed=42)

    # export gaussian splat
    _output["gs"].save_ply(f"{output_folder}/{IMAGE_NAME}.ply")
    print(f"Your reconstruction has been saved to {output_folder}/{IMAGE_NAME}.ply")


    scene_gs = make_scene(_output)
    scene_gs = ready_gaussian_for_video_rendering(scene_gs)

    video = render_video(
        scene_gs,
        r=1,
        fov=60,
        pitch_deg=15,
        yaw_start_deg=-45,
        resolution=512,
    )["color"]

    # save video as gif
    imageio.mimsave(
        os.path.join(f"{output_folder}/{IMAGE_NAME}.gif"),
        video,
        format="GIF",
        duration=1000 / 30,  # default assuming 30fps from the input MP4
        loop=0,  # 0 means loop indefinitely
    )







if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', dest='image', help='load image',  required=True)
    parser.add_argument('-m', '--mask', dest='mask', help='load mask',  required=True)
    parser.add_argument('-o', '--output', dest='output', help='output folder',  required=False)
    args = parser.parse_args()

    if not args.image or not os.path.exists(args.image):
        print("Image {} does not exist".format(args.image) )
        exit(0)
    if not args.mask or not os.path.exists(args.mask):
        print("Mask {} does not exist".format(args.mask) )
        exit(0)
    main(image=args.image, mask=args.mask,output_folder=args.output)


'''
python image_to_model.py -i notebook/images/shutterstock_stylish_kidsroom_1640806567/image.png -m notebook/images/shutterstock_stylish_kidsroom_1640806567/14.png
'''