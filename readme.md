## DOES NOT WORK

WIP chromecast receiver implementation. Authentication prevents at least the official cast API from casting to non-official receivers, but it's not clear to me if this authentication is universally implemented. microg, VLC both have bespoke cast implementations, so it's worth a shot. The implementation is incomplete, it only progressed as far as I could make stuff work (not very far).

## Research
The Google Cast protocol requires authentication of the server which makes custom server implementations impossible, however I theorize microg wouldn't implement this and thus a custom cast server implementation would work with microg phones.

[Leap Cast](https://github.com/dz0ny/leapcast) is an unmaintained implementation of the v1 cast API.

Google Cast uses [Network Service Discovery](https://developer.android.com/training/connect-devices-wirelessly/nsd) (DNS-SD).

[Avahi](https://wiki.archlinux.org/title/Avahi) is a Linux implementation of DNS-SD.

The useful part of the microg implementation of Google cast is [here](https://github.com/microg/GmsCore/blob/master/play-services-core/src/main/java/org/microg/gms/cast/CastMediaRouteProvider.java)

Based on [this](https://github.com/microg/GmsCore/blob/06fdbc34a2fa8e501eb65b833c90161efee019d6/play-services-core/build.gradle#L23) and [this](https://search.maven.org/artifact/info.armills.chromecast-java-api-v2/api-v2-raw-request), it seems microg uses [emlove's fork](https://github.com/emlove/chromecast-java-api-v2/tree/raw-request-fork) of [vitalidze/chromecast-java-api-v2](https://github.com/vitalidze/chromecast-java-api-v2) under the hood.

According to [this](https://github.com/emlove/chromecast-java-api-v2/blob/8b6d46f20875157cec22e9fb847995fd1b5a4961/src/main/java/su/litvak/chromecast/api/v2/ChromeCast.java#L61) the default port is 8009.


## Dependencies
- Linux
- Python3
- Avahi
- nss-mdns? ([this](https://github.com/emlove/chromecast-java-api-v2/blob/8b6d46f20875157cec22e9fb847995fd1b5a4961/src/main/java/su/litvak/chromecast/api/v2/ChromeCast.java#L49) implies mDNS is used and avahi warns of no "No NSS support for mDNS detected" without nss-mdns, haven't dug deeply)
- python-protobuf

## Commands
- To generate protobuf python file: `protoc ./cast_channel.proto --python_out .`

- `avahi-browse -r _googlecast._tcp` to see local chromecast devices including TXT records

- Run `./publish_service.py` and the below ncat in two separate terminals, both with root permissions

- `sudo ncat -l $(ifconfig wlan0 | grep -Po '(?<=inet )[\w\.]+') 32001 -v --ssl -c ./server.py`

VLC tries to connect but YT and other apps don't (seems microg's whole google cast implementation is currently broken). VLC fails, possibly with a cert-related error or something else.

Search logcat for "MediaRouter", that seems to indicate category->types and supportedTypes are not being set right.
