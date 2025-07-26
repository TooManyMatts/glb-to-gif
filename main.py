import trimesh
import pyrender
import numpy as np
import imageio
import os
import argparse
import subprocess


def main(args):
    """
    Convert a GLB mesh file into a spinning GIF animation.

    Parameters:
        args (argparse.Namespace): Arguments containing:
            input_path (str): Path to the input .glb file.
            nr_frames (int): Number of frames in the output GIF.
            delay (int): Frame delay in the GIF.
            size (int): Resolution (square) for rendering frames.
    """
    loaded = trimesh.load(args.input_path)

    if isinstance(loaded, trimesh.Scene):
        mesh = trimesh.util.concatenate(
            tuple(trimesh.Trimesh(vertices=g.vertices, faces=g.faces)
                  for g in loaded.geometry.values()))
    else:
        mesh = loaded

    glb_name = os.path.splitext(os.path.basename(args.input_path))[0]
    output_dir = f'{glb_name}_output'
    frames_dir = os.path.join(output_dir, 'frames')
    os.makedirs(frames_dir, exist_ok=True)

    scene = pyrender.Scene()
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
    camera_pose = np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 2],
                            [0, 0, 0, 1]])
    scene.add(camera, pose=camera_pose)

    light = pyrender.DirectionalLight(color=[1, 1, 1], intensity=4.0)
    scene.add(light, pose=camera_pose)

    renderer = pyrender.OffscreenRenderer(args.size, args.size)

    for i, angle in enumerate(np.linspace(0, 2 * np.pi, args.nr_frames, endpoint=False)):
        rotation = trimesh.transformations.rotation_matrix(angle, [0, 1, 0], mesh.centroid)
        mesh.apply_transform(rotation)

        render_mesh = pyrender.Mesh.from_trimesh(mesh, smooth=False)
        mesh_node = scene.add(render_mesh)

        color, _ = renderer.render(scene)
        imageio.imwrite(f'{frames_dir}/frame_{i:04d}.png', color)

        scene.remove_node(mesh_node)
        mesh.apply_transform(np.linalg.inv(rotation))

    subprocess.run([
        "convert",
        "-delay", str(args.delay),
        "-loop", "0",
        f"{frames_dir}/frame_*.png",
        f"{output_dir}/spinning.gif"
    ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a GLB mesh file to a spinning GIF.')
    parser.add_argument('--input_path', required=True, help='Path to input .glb file')
    parser.add_argument('--nr_frames', type=int, default=128, help='Number of frames in the GIF')
    parser.add_argument('--delay', type=int, default=10, help='Frame delay for GIF animation')
    parser.add_argument('--size', type=int, default=512, help='Resolution for output frames (square size)')

    args = parser.parse_args()
    main(args)

