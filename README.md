# `mmal-effects`

Lists the effects of MMAL's `vc.ril.image_fx`.

![Screenshot](https://github.com/Terminus-IMRC/mmal-effects/raw/gh-pages/img/snapshot.png)

<table>
  <tr> <td>none</td>       <td>solarize</td>  <td>sketch</td>      <td>emboss</td>  </tr>
  <tr> <td>oilpaint</td>   <td>hatch</td>     <td>gpen</td>        <td>pastel</td>  </tr>
  <tr> <td>colourswap</td> <td>posterise</td> <td>colourpoint</td> <td>cartoon</td> </tr>
</table>


## Requirements

You need to build/run this code on Raspberry Pi since MMAL runs only on it for
now.

In addition, you need [mmalgen](https://github.com/Terminus-IMRC/mmalgen) to
generate C code.


## Building

```
$ git clone https://github.com/Terminus-IMRC/mmal-effects.git
$ git clone https://github.com/Terminus-IMRC/mmalgen.git
$ cd mmal-effects/
$ ./gengen.py | ../mmalgen/mmalgen.py >out.c
$ export PKG_CONFIG_PATH=/opt/vc/lib/pkgconfig
$ gcc out.c `pkg-config --cflags --libs mmal` -I../mmalgen/
```


## Running

```
$ ./a.out
```
