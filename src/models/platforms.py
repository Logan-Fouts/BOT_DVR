from dataclasses import dataclass


@dataclass
class StreamingPlatform:
    """Defines a basic streaming platform data class."""

    name: str
    img_ll: str
    img_end: str
    move_left: int
    move_top: int

    def __post_init__(self):
        if not self.name:
            raise ValueError("Name cannot be empty")
        if not self.img_ll:
            raise ValueError("Image path cannot be empty")


@dataclass
class Disney(StreamingPlatform):
    """Disney instance of a streaming platform."""

    def __init__(self):
        super().__init__(
            name="Disney",
            img_ll="assets/images/ll_images/disney_ll.png",
            img_end="assets/images/end_images/disney_end.png",
            move_left=30,
            move_top=25,
        )


@dataclass
class Netflix(StreamingPlatform):
    """Netflix instance of a streaming platform."""

    def __init__(self):
        super().__init__(
            name="Netflix",
            img_ll="assets/images/ll_images/netflix_ll.png",
            img_end="assets/images/end_images/netflix_end.png",
            move_left=80,
            move_top=65,
        )


class PlatformFactory:
    """Streaming platform factory that allows creation of differnt types of platforms."""

    @staticmethod
    def create_platform(platform_name: str) -> StreamingPlatform:
        """
        Depending on the name of the platform instntiates a new platform data type to be used.
        """
        if platform_name == "Disney":
            return Disney()
        if platform_name == "Netflix":
            return Netflix()
        raise ValueError(f"Unknown platform: {platform_name}")
