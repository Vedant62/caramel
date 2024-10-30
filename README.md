# caramel

basic image processing directly from your cli 
(only works on mac devices as I have been experimenting with applescript for better ux)
> to replicate, make the script executable and move to `/usr/local/bin/<your-tool-name>`

<img width="1162" alt="image" src="https://github.com/user-attachments/assets/b8d31355-31e2-423e-8fea-31acb40a133d">

> you can change to any interpreter you want and install `numpy`, `matlplotlib` and `scipy`

- prompts finder to choose an image
- can preview the image before saving
- can save to destination location using finder

1. Brightness:
   - Range: -255 to 255
   - Recommended: -100 to 100
   - Default: N/A (required parameter)

2. Blur:
   - Radius: 1 to 5
   - Sigma: 0.1 to 5.0
   - Recommended: radius=2, sigma=1.5

3. Sharpen:
   - Range: 0.1 to 5.0
   - Recommended: 0.5 to 2.0
   - Values > 2.0 may create artifacts

4. Rotate:
   - Only accepts: 90, 180, 270
   - Values represent degrees counter-clockwise

5. Flip:
   - Only accepts: "horizontal" or "vertical"