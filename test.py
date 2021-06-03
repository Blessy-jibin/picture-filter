import unittest

import mock
import pytest
from PIL import UnidentifiedImageError

import filter
import image


class TestImage(unittest.TestCase):
    @mock.patch("image.PILImage")
    def setUp(self, mock_PILImage):
        self.image = image.Image("path/image.jpg")
        self.mock_PILImage = mock_PILImage
        self.mock_PILImage.open.assert_called_once_with("path/image.jpg")

    @mock.patch("image.PILImage")
    def test_image(self, mock_PILImage):
        mock_PILImage.open.side_effect = UnidentifiedImageError(
            "cannot identify image file 'test.txt'"
        )
        with pytest.raises(UnidentifiedImageError) as excinfo:
            image.Image("path/test.txt")
        assert excinfo.value.args[0] == "cannot identify image file 'test.txt'"

    def test_rotate(self):
        self.image.rotate(90)
        self.mock_PILImage.open().rotate.assert_called_once_with(90)

        with pytest.raises(ValueError) as excinfo:
            self.image.rotate("text")
        assert excinfo.value.args[0] == ("Invalid value 'text' for rotate")

    def test_gray_scale(self):
        self.image.gray_scale()
        self.mock_PILImage.open().convert.assert_called_once_with("1")

    @mock.patch("image.PILImage")
    def test_over_lay(self, mock_PILImage2):
        self.image.overlay("path/overlay_image.png")
        mock_PILImage2.open.assert_called_once_with("path/overlay_image.png")
        args = self.mock_PILImage.open().paste.call_args[0]
        assert args[1] == (0, 0)

        with pytest.raises(TypeError) as excinfo:
            self.image.overlay("path/overlay_image.jpg")
        assert excinfo.value.args[0] == (
            "File 'path/overlay_image' is not .png formatted"
        )

        with pytest.raises(TypeError) as excinfo:
            rgba_image = mock.MagicMock()
            rgba_image.filename = "overlay_img.png"
            rgba_image.getextrema.return_value = [(255, 255)]
            mock_PILImage2.open().convert.return_value = rgba_image
            self.image.overlay("path/overlay_img.png")

        error = "Image 'overlay_img.png' is not transparent"
        assert excinfo.value.args[0] == (error)

    def test_save(self):
        self.image.save("path/output_file.png")

        with pytest.raises(TypeError) as excinfo:
            self.image.save("path/output_file.gif")
        assert (
            excinfo.value.args[0]
            == "File 'path/output_file' is not .jpg or .png formatted"
        )


class TestFilter(unittest.TestCase):
    @mock.patch("filter.sys")
    @mock.patch("filter.image")
    def test_filter(self, mock_image, mock_sys):
        mock_sys.argv = ["test_script.py", "input.png", "output.png"]
        filter.main()

        mock_sys.argv = ["test_script.py", "--help"]
        filter.main()
        mock_sys.exit.assert_called_once()

        mock_sys.argv = [
            "test_script.py",
            "--rotate",
            90,
            "input.png",
            "output.png",
        ]
        filter.main()
        mock_image.Image().rotate.assert_called_once_with(90)

        mock_sys.argv = [
            "test_script.py",
            "--gray_scale",
            "input.png",
            "output.png",
        ]
        filter.main()
        mock_image.Image().gray_scale.assert_called_once_with()

        mock_sys.argv = [
            "test_script.py",
            "--overlay",
            "overlay_img.png",
            "input.png",
            "output.png",
        ]
        filter.main()
        mock_image.Image().overlay.assert_called_once_with("overlay_img.png")

    @mock.patch("filter.sys")
    @mock.patch("filter.image")
    def test_filter_with_errors(self, mock_image, mock_sys):
        with pytest.raises(SyntaxError) as excinfo:
            mock_sys.argv = ["test_script.py"]
            filter.main()
        assert excinfo.value.args[0] == (
            "Missing required arguments 'source_image' and 'output_image'"
        )

        with pytest.raises(SyntaxError) as excinfo:
            mock_sys.argv = ["test_script.py", "input.png"]
            filter.main()

        error = "Missing required argument 'output_image'"
        assert excinfo.value.args[0] == (error)

        with pytest.raises(SyntaxError) as excinfo:
            mock_sys.argv = [
                "test_script.py",
                "--message",
                "Messgae",
                "input.png",
                "output.png",
            ]
            filter.main()


if __name__ == "__main__":
    unittest.main()
