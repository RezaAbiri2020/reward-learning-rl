"""Replay pool that also stores images from the environment.

TODO.hartikainen: This is still work-in-progress until I can figure out a
reasonable apis between the sampler, pool, observations (images) preprocessor,
and the policy.
"""

import os
from PIL import Image

import numpy as np

from rllab.core.serializable import Serializable

from .replay_pool import ReplayPool
from .simple_replay_pool import SimpleReplayPool


class ImageReplayPool(SimpleReplayPool, Serializable):
    def __init__(self,
                 image_directory,
                 *args,
                 image_format='png',
                 **kwargs):
        Serializable.quick_init(self, locals())
        super(ImageReplayPool, self).__init__(*args, **kwargs)

        self.image_directory = image_directory
        self.image_format = image_format

        fields = {
            'images': {
                'shape': [2], # (rollout_id, step_id)
                'dtype': 'uint64'
            },
        }

        self.add_fields(fields)

    def image_location(self, image_id):
        episode, step = image_id
        image_directory = "{}/{}".format(self.image_directory, episode)
        image_location = "{}/{}.{}".format(
            image_directory, step, self.image_format)

        return image_location

    def save_image(self, image_id, image_np):
        """Save image array (image_np) as to disk."""

        image_location = self.image_location(image_id)

        if not os.path.exists(os.path.dirname(image_location)):
            os.makedirs(os.path.dirname(image_location))

        image = Image.fromarray(image_np)
        image.save(image_location)

    def add_sample(self, **kwargs):
        """Save image to file and save reference to it in replay pool"""

        (image_id, image_np) = kwargs.pop('images')
        self.save_image(image_id, image_np)

        super(ImageReplayPool, self).add_sample(**kwargs, image_ids=image_id)