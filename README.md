# GF-Complete for RACE

This repo provides scripts to custom-build the
[GF-Complete library](https://github.com/ceph/gf-complete) for RACE.

## License

The GF-Copmlete library is licensed under the 3-Clause BSD license.

Only the build scripts in this repo are licensed under Apache 2.0.

## Dependencies

GF-Complete has no dependencies on any custom-built libraries.

## How To Build

The [ext-builder](https://github.com/tst-race/ext-builder) image is used to
build GF-Complete.

```
git clone https://github.com/tst-race/ext-builder.git
git clone https://github.com/tst-race/ext-gf-complete.git
./ext-builder/build.py \
    --target linux-x86_64 \
    ./ext-gf-complete
```

## Platforms

GF-Complete is built for the following platforms:

* `linux-x86_64`
* `linux-arm64-v8a`
* `android-x86_64`
* `android-arm64-v8a`

## How It Is Used

GF-Complete is a dependency for the Jerasure custom-built library.
