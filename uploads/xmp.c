
#include <mlx.h>


int main(int ac, char *argv[])
{
	if (ac != 2)
		return 0;
	int	width, height;
	void *mlx = mlx_init();
	void *win = mlx_new_window(mlx, 512, 512, "XMP");
	void *image = mlx_xpm_file_to_image(mlx, argv[1], &width, &height);

	printf("%i %i\n", width, height);
	mlx_put_image_to_window(mlx, win, image, 0, 0);
	mlx_loop(mlx);
	return 0;
}
