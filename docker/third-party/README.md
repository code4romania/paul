# Third-party dependencies for Docker images

## UV

UV is the Python package manager for the Docker images.
It is used to install and manage back-end dependencies.

### Download link

[Installer file](https://astral.sh/uv/install.sh)

### Updating by curl

To update the UV package, run the following command:

```bash
curl -LsSf https://astral.sh/uv/install.sh > ./docker/third-party/uv/installer.sh
```

Or, just open the download link in your browser and save the file as `installer.sh` in the `docker/third-party/uv` directory.
