# dot2nn - Define your Neural Network with DOT

`dot2nn` is a script to compile DOT language to Neural Network (NN) Definition code for various frameworks.
(_TODO_: Supported frameworks are keras, pytorch, ...)

## [DOT?](https://www.graphviz.org/doc/info/lang.html)

DOT-like language

_TODO_: Spec

## Usage?

_TODO_: Currently, the script doesn't write as a portable script. Please run by `python ./main.py ...`

```sh
dot2nn -T<type> < source.dot
```

## Examples of NN Definition?

```dot
# A single sequential network
nn {
    Input -> l1 [net=reshape];  # flatten from 2d to 1d
    l1 -> l2 [net=linear];
    l2 -> Output [net=linear];
    Input [shape=28*28];
    l1 [shape=100 activation=relu regularizer_l2=0.1];
    l2 [shape=100 activation=relu regularizer_l2=0.01];
    Output [shape=10 activation=softmax];
}
#-style or
//-style commeent out available
```

```dot
# AutoEncoder
encoder {
    Input -> h -> Output;  // net=linear in default, and edges can be write connectedly if the attributes are same
    Input [shape=28*28]
    h [shape=100 activation=sigmoid]
    Output [shape=64]  # activation in default
}

decoder {
    Input -> l1
    l1 -> l2 [net=reshape]
    l2 -> Output [net=conv kernel=5]
    Input [shape=10]
    l1 [shape=900]
    l2 [shape=30*30]
    Output [shape=28*28]
}

autoencoder {
    # combine of encoder and decoder
    Input -> z [net=encoder]
    z -> Output [net=decoder]
}
```

```dot
# An example of multiple inputs/outputs model
two_in_two_out {
    Input -> {x1 x2} [net=copy];  # Destructuring assignment; (x1, x2) = Input
    x1 -> z1;
    x2 -> z2;
    {z1 z2} -> Output [net=copy];  # Assignment; Output = tuple(z1, z2)
    x1 [shape=16]
    x2 [shape=16]
    z1 [shape=8]
    z2 [shape=8]
}

model {
    Input -> x1;
    Input -> x2;  # NOTE: cannot write as `Input -> {x1 x2}` since linear is 1-in/1-out
    {x1 x2} -> {z1 z2} [net=two_in_two_out];
    {z1 z2} -> Output [net=add]
}
```

```dot
# Variational AutoEncoder

encoder {
    # 1-in 2-out
    Input -> z [net=encoder]
    z -> mean
    z -> var
    Input [shape=100]
    mean [shape=64]
    var [shape=64]
    {mean var} -> Output [net=copy]
}

decoder {
    Input -> h -> Output
    Input [shape=64]
    h [shape=100 activation=relu]
    Output [shape=100]
}

vae {
    # combine of encoder, sampling and decoder
    Input -> {m v} [net=vae_encoder]
    {m v} -> z [net=gaussian_sampling]
    z -> Output [net=decoder]
}
```

```dot
# GAN
generator {
}

discriminator {
}
```
