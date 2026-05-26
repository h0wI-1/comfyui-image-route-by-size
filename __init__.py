import torch


class ImageRouteBySize:
    """
    Routes an image to one of two outputs based on width.
      - large:        the image when width > max_width, else a 1x1 white placeholder
      - small:        the image when width <= max_width, else a 1x1 white placeholder
      - needs_resize: INT  1 = large path active, 0 = small path active

    Use ImagePickByFlag downstream to merge the two paths back into one.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image":     ("IMAGE",),
                "max_width": ("INT", {"default": 1248, "min": 1, "max": 8192, "step": 1}),
            }
        }

    RETURN_TYPES  = ("IMAGE", "IMAGE", "INT")
    RETURN_NAMES  = ("large", "small", "needs_resize")
    FUNCTION      = "route"
    CATEGORY      = "image/routing"

    def route(self, image, max_width):
        w = image.shape[2]
        placeholder = torch.ones(1, 1, 1, 3, dtype=image.dtype, device=image.device)
        if w > max_width:
            return (image, placeholder, 1)
        else:
            return (placeholder, image, 0)


class ImagePickByFlag:
    """
    Merges the two outputs of ImageRouteBySize back into one image.
      needs_resize = 1  ->  returns image_a  (came from the resize / large path)
      needs_resize = 0  ->  returns image_b  (came from the direct / small path)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_a":      ("IMAGE",),
                "image_b":      ("IMAGE",),
                "needs_resize": ("INT",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION     = "pick"
    CATEGORY     = "image/routing"

    def pick(self, image_a, image_b, needs_resize):
        return (image_a if needs_resize == 1 else image_b,)


NODE_CLASS_MAPPINGS = {
    "ImageRouteBySize": ImageRouteBySize,
    "ImagePickByFlag":  ImagePickByFlag,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageRouteBySize": "Image Route By Size",
    "ImagePickByFlag":  "Image Pick By Flag",
}
