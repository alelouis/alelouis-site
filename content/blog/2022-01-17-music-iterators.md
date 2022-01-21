---
title: Rebuilding arpeggiators with Rust iterators
draft: true
---

I often play with arpeggiators, whether they come from my analog synthesizer or with the Ableton built-in plugin. Arpeggiators are cool in their ability to bring movement to chords, bridging a gap between harmony and melody. From their rhythmic nature, they also are useful when you are looking to lock the tempo in a particular composition.

## Arpeggia-what ?

> An arpeggiator can be defined as something that builds a sequence of notes out of a given collection of notes.

 Let's take a basic chord : **C Major**. The **C** major chord is composed of one root note, here **C** (or Do), and two intervals : a major third (**E** or mi) and a perfect fifth (**G** or Sol).

An arpeggiator applied to the chord C Major would create a sequence out of its notes **{C, E, G}**.
The simplest sequence one can think about is the ascending arpeggio : **C**, then **E**, then **G**.

Of course, imagination is the limit here (and combinatorics too but shh).

## Mumuse

I recently started working on a music theory library in Rust : **mumuse**. The developement repository is [available](https://github.com/alelouis/mumuse) on Github.

As the time of writing, the library provides building blocks for elementary note, chord and scale manipulations. I often feel stuck in front of my DAW when I want to explore music ideas in a procedural way. Being an OK programmer, I can explore many different ideas as code and often quicker than I would in front of a piano (which I do too, but with different goals).

As soon as I released an early version of **mumuse**, I wanted to use it in a practical way (other than writing test modules, I mean). Then came the idea of recreating some of the arpeggiator modes in Ableton's default plugin. The constraint I would impose to myself being to do that with only **iterators** and **mumuse**.

<img style="margin: 0 auto; display: block; width : 30%;" src="../../images/music_iterators/arp_ableton.png">

**<center>Ableton default arpeggiator modes</center>**

## Itera-what ? 

Well, not going through the horrendous details, an iterator is something that iterates through an iterable, one element at a timee. Yes, my definitions today are top notch (really bad and not complete what so ever, don't take for granted what I say). 

Consider this list of integer : `[1, 2, 3, 4]`. An iterator would go through all the values independently, in order. What's interesting is that we can, in a functional programming fashion, modify the behavior or effect of an iterator. We can apply **iterators methods**. In Rust, iterators methods can be one of two types : **adapters** or **consumers**. 

**Adapters** methods return other iterators while consumers *consume* the iterator and output values, vectors or other things that are not iterators. E.g with a popular adapter method : `map` : 

```rust 
let var = (1..4).map(|value| value * 2);
```

The `map` method takes as an argument a **closure** (anonymous function) the will be applied on each value encountered in `var`. In this example, the closure simply multiplies the current value by `2`. Note that the computation isn't actually performed, the `var` isn't equal to `[2, 3, 6, 8]` after this line. Instead, `var` is **lazy evaluated** : each value will be computed only when their are needed in the program.

**Consumers** eat that damn iterator and poop another useful value (yea, not the best metaphor). The simplest consumer method could be the `sum` method.

```rust 
let var_sum= (1..4).map(|value| value * 2).sum();
```
The `sum` method is applied to the iterator , itself adapted with a `map`. So `var_sum` will be equal, after this line, to the sum of `[2, 3, 6, 8]`, that is to say `19`.

You know well enough to go through the next section : making arpeggiators out of iterators !

## Iterators are all you need

We need some chord to iterate on. My library **mumuse** exposes the `Chord` struct, which itself contains a vector of `Note` structs. I will use a **D Minor 7th** chord. This chord happens the natural chord built from the 2nd degree of the **C Major** scale. This isn't a music theory 101 article so here is the code to create such chord.

```rust
pub fn get_notes(n: usize) -> Vec<Note> {
    Scale::major(Note::try_from("C3").unwrap()).two(n).notes
}
```

The function `get_notes()` use the `Scale` struct in order to retrieve the second (`two`) chord with `n` notes. The field `notes` of the `Chord`, which is of type `Vec<Note>`, is then returned. All is set up in order to start building arpeggiators !

### Up

This one is the easiest. The **Up** arpeggiator plays notes bottom up. This is the default behavior of an iterator on a vector if the vector contains ascending notes (it does), so the implementation is straightforward.

```rust
let up = get_notes(n).into_iter();
```
Then, I did two things to appreciate the result.
- First, generating the sheet music through [LilyPond](http://lilypond.org/) by outputting a **Tiny Notation** from the iterator. 
- Also, I sent the note through Midi into an [Ableton Live](https://www.ableton.com/en/) instrument to hear the result.

The outputs are below, I will do the same for each arpeggiator we cover.

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/up.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/up.wav" type="audio/wav">
</audio> 

### Down

The **Down** iterator goes the other way. The `notes` then need to be iterated backwards. We can use the `.rev()` method to reverse the order of iteration.

```rust
let down = get_notes(n).into_iter().rev();
```

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/down.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/down.wav" type="audio/wav">
</audio> 

### Up Down

The **Up Down** arpeggiator, not to be confused with Up **And** Down, goes up then down but without the last note of the up run and the first of the down. This avoids the repetition of the higher and lower notes. We use here the `.take(n)` method which only iterates on the first `n` elements. Then we use the `.chain()` method the concatenate the cropped **Up** and **Down** iterators.

```rust
let up_down = get_notes(n)
    .into_iter()
    .take(n - 1)
    .chain(get_notes(n).into_iter().rev().take(n - 1));
```

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/up_down.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/up_down.wav" type="audio/wav">
</audio> 

### Down Up

**Down Up** is simply the reversed version of **Up Down**.

```rust
let down_up = get_notes(n)
    .into_iter()
    .rev()
    .take(n - 1)
    .chain(get_notes(n).into_iter().take(n - 1));
```

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/down_up.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/down_up.wav" type="audio/wav">
</audio> 

### Up And Down

While the **Up Down** variant was avoiding the higher and lower note repetition, the **Up And Down** doesn't care, so it is simpler.

```rust
let up_and_down = get_notes(n)
    .into_iter()
    .chain(get_notes(n).into_iter().rev());
```

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/up_and_down.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/up_and_down.wav" type="audio/wav">
</audio> 

### Down And Up

Same idea, in the other direction.

```rust
let down_and_up = get_notes(n)
    .into_iter()
    .rev()
    .chain(get_notes(n).into_iter());
```

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/down_and_up.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/down_and_up.wav" type="audio/wav">
</audio> 

### Converge

Ok, this one is more interesting. The **Converge** mode go from extremities towards the inner notes. From an iterator point of view, we can implement this by **interleaving** the **Up** and **Down** iterators and taking only the first `n` elements to avoid diverging from mid point.

**Interleaving** is the process of alternating some values with others. If you were to interleave `[0, 0, 0, 0]` with `[1, 1, 1, 1]`, you would get `[0, 1, 0, 1, 0, 1, 0, 1]`.

```rust
let converge = get_notes(n)
    .into_iter()
    .interleave(get_notes(n).into_iter().rev())
    .take(n);
```

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/converge.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/converge.wav" type="audio/wav">
</audio> 

### Diverge

```rust
let diverge = get_notes(n)
    .into_iter()
    .interleave(get_notes(n).into_iter().rev())
    .skip(n)
    .take(n);
```

Well, **Diverge** goes the other way. Starting from inner notes and expanding towards higher and lower notes. Just before I said we avoided diverging by stopping at mid point, because by **interleaving** the **Up** and **Down** iterators, some sort of cross pattern is created : first the notes converge and then they diverge from each others. 

From this observation, we can simply use the same idea we used in **Converge**, skip the converge part with `.skip()`, and finally take the next `n` elements that are diverging.

We could also `.rev()` the converge part, but that's too easy.

 <img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/diverge.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/diverge.wav" type="audio/wav">
</audio> 

### Pinky Up

Another interesting one and, I must admit, one of my favorites. The **Pinky Up** mode emulates your pinky playing the higher note in between a **Up** run. This creates a pedal effect, which I love.

For this one, I use the `.intersperse()`, which is a bit like `.interleave()`, the only difference being that the first one takes as input a single value. This single value is added in-between each element of the original iterator.

I don't know if this proper english, but that's how I understand it. Anyhow, `.intersperse()` is clearly what we need in order to fit this higher note `get_notes(n)[n - 1]` in-between the **Up** run.

Also, we need to make sure we take the correct number of elements (`2 * (n - 1)`), otherwise we would get the last chord's note two times (the note itself and the ultimate interspersed note).

```rust
let pinky_up = get_notes(n)
    .into_iter()
    .take(n)
    .intersperse(get_notes(n)[n - 1])
    .take(2 * (n - 1));
```

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/pinky_up.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/pinky_up.wav" type="audio/wav">
</audio> 

### Pinky Up Down

Why only go **Up** ? In the same fashion as the **Up Down**, we can intersperse the higher note with the **Up Down** iterators, also making sure we don't take extra notes that would invalidate the pattern.

```rust
let pinky_up_down = get_notes(n)
    .into_iter()
    .take(n - 1)
    .chain(get_notes(n).into_iter().take(n - 2).rev())
    .intersperse(get_notes(n)[n - 1])
    .take(4 * (n - 2));
```

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/pinky_up_down.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/pinky_up_down.wav" type="audio/wav">
</audio> 

### Thumb Up

If you followed along **Pinky Up**, this one should be easy. We apply the same idea but with the lower note of the chord. As a little detail, we still need to pay attention and skip the first element after intersperse in order to avoid the first note repetition.

```rust
let thumb_up = get_notes(n)
    .into_iter()
    .intersperse(get_notes(n)[0])
    .skip(1)
    .take(2 * (n - 1));
```

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/thumb_up.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/thumb_up.wav" type="audio/wav">
</audio> 

### Thumb Up Down

This last one uses nearly everything we covered, it's a pretty one :)

```rust
let thumb_up_down = get_notes(n)
    .into_iter()
    .take(n)
    .chain(get_notes(n).into_iter().take(n - 1).rev())
    .intersperse(get_notes(n)[0])
    .skip(1)
    .take(4 * (n - 2));
```

<img style="margin: 0 auto; display: block; width : 70%;" src="../../images/music_iterators/thumb_up_down.svg">
<audio style="margin: 0 auto; display: block; width : 70%;" controls>
    <source src="../../images/music_iterators/thumb_up_down.wav" type="audio/wav">
</audio> 

## Conclusion

This was fun. It was a good exercise for me, and I learned several things :
- I had to analyse arpeggiators modes note by note and I feel like I understand them perfectly now.
- Playing with Rust iterators methods, which I will try to (ab)use more in my code style.
- Building some fancy scripting utility for generating sheets automatically using [mumuse](https://github.com/alelouis/mumuse), [music21](https://web.mit.edu/music21/) and [LilyPond](http://lilypond.org/) 

**All the code used to produce sheet music, MIDI and arpeggiators is available [here](https://github.com/alelouis/arpeggiators-and-iterators).**

I hope you liked / learned something along this article. See you next time.