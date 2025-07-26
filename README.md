# 🎞️ glb-to-gif

A minimal Python tool to convert 3D `.glb` mesh files into spinning animated GIFs.

## 📦 Included Files

- [`main.py`](main.py): Generates frames and creates a spinning GIF.
- [`cid_13.glb`](cid_13.glb): Sample mesh file (Pentagonal Hexecontahedron).
- [`wid_27.glb`](wid_27.glb): Sample mesh file (Second Stellation of Icosahedron).

## 🚀 Quick Start

**Install dependencies:**

```bash
pip install trimesh pyrender imageio[ffmpeg]
sudo apt install imagemagick
```

**Generate GIF:**

```bash
python main.py --input_path cid_13.glb --nr_frames 128 --delay 10 --size 512
```

- Frames and GIF will be saved in `<mesh_name>_output/`.

## 🎬 Sample Output

Generated spinning GIF:

```markdown
![Sample GIF](wid_27_output/spinning.gif)
```
