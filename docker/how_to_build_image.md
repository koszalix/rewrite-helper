1. Before container building check if program pass all tests
2. [See emulator container](https://github.com/tonistiigi/binfmt#installing-emulators)
3. Install emulators

```bash
docker run --privileged --rm tonistiigi/binfmt --install all
```

2. Create builder

```bash
docker buildx create --name rewrite-builder --use
```

3. Ensure if all needed architectures are supported

```bash
docker buildx inspect --bootstrap
```

4. Create image for all architectures or...

```bash
docker buildx build --platform linux/amd64,linux/amd64/v2,linux/arm64,linux/ppc64le,linux/s390x,linux/386,linux/arm/v7,linux/arm/v6,linux/arm/v8 -t koszalix:rewrite-helper . --push
```

5. for most used architectures

```bash
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v8 -t koszalix/rewrite-helper:latest --push .
```