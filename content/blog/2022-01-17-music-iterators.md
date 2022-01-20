---
title: Rebuilding arpeggiators with Rust iterators
draft: true
---

I often play with arpeggiators, whether they come from my analog synthesizer or with the Ableton built-in plugin. Arpeggiators are cool in their ability to bring movement to chords, bridging a gap between harmony and melody. From their rhythmic nature, they also are useful when you are looking to lock the tempo in a particular composition.

## Arpeggia-what ?

> An arpeggiator can be defined as something that builds a sequence of notes out of a given collection of notes.

 Let's take a basic chord : **C Major**. The **C** major chord is composed of one root note, here **C** (or Do), and two intervals : a major third (**E** or mi) and a perfect fifth (**G** or Sol).

An arpeggiator applied to the chord C Major would create a sequence out of its notes {C, E, G}.
The simplest sequence one can think about is the ascending arpeggio : C, then E, then G.

Of course, imagination is the limit here (and combinatorials too but shh).

## Mumuse

I recently started working on a music theory library in Rust : **mumuse**. The developement repository is [available](https://github.com/alelouis/mumuse) on Github.

As the time of writing, the library provides building blocks for elementary note, chord and scale manipulations. I often feel stuck in front of my DAW when I want to explore music ideas in a procedural way. Being an OK programmer, I can explore many different ideas as code and often quicker than I would in front of a piano (which I do too, but with different goals).

As soon as I released an early version of **mumuse**, I wanted to use it in a practical way (other than writing test modules, I mean). Then came the idea of recreating some of the arpeggiator modes in Ableton's default plugin. The constraint I would impose to myself being to do that with only **iterators** and **mumuse**.

## Itera-what ? 

Well, not going through the horrendous details, an iterator is something that iterates through an iterable, value by value. Yes, my definitions today are top notch (really bad and not complete what so ever, don't remember what I say). 

Consider this list of integer : `[1, 2, 3, 4]`. An iterator would go through all the values independently. What's interesting is that we can, in a functional fashion, modify the behavior or effect of an iterator. We can apply **iterators methods**. In Rust, iterators methods can be one of two types : **adapters** or **consumers**. 

**Adapters** methods return other iterators while consumers *consume* the iterator and output values, vectors or other things that are not iterators. E.g with a popular adapter method : `map` : 

```rust 
let var = (1..4).map(|value| value * 2);
```

The `map` method takes as an argument a closure (anonymous function) the will be applied on each value encountered in `var`. In this example, the closure simply multiplies the current value by `2`. Note that the computation isn't actually performed, the `var` isn't equal to `[2, 3, 6, 8]` after this line. Instead, `var` is lazy evaluated : each value will be computed only when their are needed in the program.

**Consumers** eat that damn iterator and poop another useful value (yea, not the best metaphor). The simplest consumer method could be the `sum` method.

```rust 
let var_sum= (1..4).map(|value| value * 2).sum();
```
The `sum` method is applied to the iterator , itself adapted with a `map`. So `var_sum` will be equal, after this line, to the sum of `[2, 3, 6, 8]`, that is to say `19`.

You know well enough to go through the next section : making arpeggiators out of iterators !

## Iterators are all you need

### Up

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/up.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/up.wav" type="audio/wav">
</audio> 

### Down

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/down.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/down.wav" type="audio/wav">
</audio> 

### Up Down

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/up_down.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/up_down.wav" type="audio/wav">
</audio> 

### Down Up

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/down_up.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/down_up.wav" type="audio/wav">
</audio> 

### Up And Down

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/up_and_down.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/up_and_down.wav" type="audio/wav">
</audio> 

### Down And Up

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/down_and_up.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/down_and_up.wav" type="audio/wav">
</audio> 

### Converge

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/converge.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/converge.wav" type="audio/wav">
</audio> 

### Diverge

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/diverge.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/diverge.wav" type="audio/wav">
</audio> 

### Pinky Up

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/pinky_up.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/pinky_up.wav" type="audio/wav">
</audio> 

### Pinky Up Down

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/pinky_up_down.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/pinky_up_down.wav" type="audio/wav">
</audio> 

### Thumb Up

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/thumb_up.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/thumb_up.wav" type="audio/wav">
</audio> 

### Thumb Up Down

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/thumb_up_down.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/thumb_up_down.wav" type="audio/wav">
</audio> 