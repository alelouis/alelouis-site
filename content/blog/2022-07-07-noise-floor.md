---
title: Noise floor and Power Spectrums
---

When dealing with sampled signals, signal processing engineers often make use of various transforms in order to analyze the signal.
One of them which is of great value is the Power Spectrum. I already made a post on how to compute it, so in this article I will explain how to and not to measure noise floors using a simple PSD.

## Generating a signal
First, we'll generate a basic signal : a complex exponential wave. Why are we using complex signals ? Well there are a lot of good reasons, the one I will give today is that it conceptually fits a certain type of [modulation/demodulation](https://www.cs.princeton.edu/courses/archive/spring19/cos463/lectures/L12-digital.pdf) scheme used in modern radio frequency transponders.

I will put every line of Python code I write in order to be as complete as possible.

I choose a sampling frequency $f_s$ of $1\text{ MHz}$ and a center frequency $f$ of $f_s/16$.

```python
n_samples = 2**16
fs = 1e6
t = np.arange(n_samples)/fs
f = fs/16
p = 1 # power of signal
signal = np.sqrt(p)*np.exp(2j*np.pi*f*t)
```
Below is a plot of real and imaginary parts for the first $50$ samples.

<img style="margin: 0 auto; width : 90%;" src="../../images/noise-floor/temporal.svg">
<center>Figure $1$: signal of interest</center>

In order to compute the power of this signal, we can (from what we know) either take the mean of squares values (or variance in the case of 0-mean signal) or compute it from theory.

From theory, the most common knowledge would be that the RMS (Root Mean Squared) value of a cosine wave of amplitude $A$ is $A/\sqrt2$, its power is the square of that (mean squared), so $A^2/2$.

Because $Ae^{jwt}$ is also $A\cos(wt)+jA\sin(wt)$, $Ae^{jwt}$ has actually twice the power of a single cosine wave, that is to say $A^2$.

In our case, $A=1$, so it doesn't change anything, but as a quick reminder, to generate an complex wave of power $C$, its amplitude should be $\sqrt{C}$.

Now suppose we are to simulate a noisy channel, we would add a (again complex) gaussian noise.

```python
p_n = 1 # noise power
noise = np.sqrt(p_n/2)*(randn(n_samples)+1j*randn(n_samples))
signal += noise
```

We are adding a complex noise of power $p_n$, we are also dividing by $\sqrt{2}$ because each `randn` noise has a variance of $1$, i.e. a power of $1$.

This is our noisy signal.

<img style="margin: 0 auto; width : 90%;" src="../../images/noise-floor/temporal-noisy.svg">
<center>Figure $2$: noisy signal</center>

Ouch, our signal-to-noise ratio (SNR) seems bad, it is actually of $1/p_n=1$ (in linear), which means that the signal and noise have the same power. In the temporal domain, we can't even see our signal. Going to frequency domain might help us here.

## Going full frequency mode
In order to be basic about it, I will compute the PSD by averaging severals FFT of size `nfft` magnitudes squared ([Welch's method](https://ccrma.stanford.edu/~jos/sasp/Welch_s_Method.html) without overlap or windowing).

```python
nfft = 2**8
signal = reshape(signal, (signal.size//nfft, nfft))
signal_fft = fft.fft(signal, axis = 1)/nfft
psd = np.mean(np.abs(signal_fft)**2, axis = 0)
psd_db = 10*np.log10(psd)
```

On the third line, I normalize the FFT in order to conserve the energy of the transform, that is to say that `sum(signal**2)==sum(abs(signal_fft)**2)`.

Caution here, I call this a PSD with a D for Density, while other sources might call this simply a power spectrum, more details on that later.

This is the result :

<img style="margin: 0 auto; width : 90%;" src="../../images/noise-floor/psd.svg">
<center>Figure $3$: PSD</center>

Our signal is back. What we are actually computing here is the amount of power contained in each of the `nfft` bins, in the frequency domain. Because our complex wave theoretically exist only at frequency $f$, all its power falls in one bin (only in theory, because we are dealing with finite signals here). Everywhere else, noise dominates. As a note, a *white* gaussian noise is called white because it has a flat frequency response, which means each bin have roughly the same power.

The main take away here is that going to the frequency domain makes it really easier for us to analyze the signal, now let's deduce quantitative information from the PSD.

The peak amplitude is our wave power (and a negligible bit of noise power), here $0 \text{ dBW} = 10\log_{10}(1)=p$, this is all fine. 

Can we estimate the noise power from here ? Well the amplitude of noise seems to be around $-24\text{ dBW}$, which is... $0.0079 \text{ W}$ ? Hm, shouldn't we multiply by the number of bins, or `nfft` ? $$10\log_{10}{(-24)}\cdot2^8 \approx 1.019154 \text{ W}.$$ Close to $p_n$ !

So, is it all done ? Not completely: noise power is often characterized by its normalized value, the Noise Spectral Density, notated $N_0$. The SI unit of $N_0$ is $\text{W/Hz}$, and is often computed from the following equation :

$$N_0=k_bT$$

With $k_b$ the Boltzmann's constant in $\text{J/K}$ and $T$ the receiver temperature in $\text{K}$. This gives us Joules, or Watts seconds, or Watts per Hertz.

The problem is that, the way I computed the PSD *doesn't display* the $N_0$, I can't get it from the plot. This is a common mistake, assuming that the read value of the noise floor is the value of its spectral density. In a sense, it is, but not normalized in Hertz !

Because we are computing a `nfft` FFT over a complex sampling rate of $f_s$, each bin represents the noise power in $f_s/\text{nfft}$ Hertz. Actually we know what the $N_0$ should be, it's $p_n/f_s=-60\text{ dBW/Hz}$. Which is way off the value $-24$ we are at.

So, normalize the PSD and everything is fine ? Here is the same PSD, but divided by $f_s/\text{nfft}$ in order to get per Hertz values:

<img style="margin: 0 auto; width : 90%;" src="../../images/noise-floor/psd_norm.svg">
<center>Figure $3$: PSD normalized</center>

The normalized one is the curve in `cyan`. Everything is lower and we finally observe our real $N_0$ on the y-axis. But notice that our wave peak isn't at the right value anymore: if we were to estimate its power from peak amplitude, it would be completely wrong.

So ? You can't have both ! Apart from the case where you choose $\text{nfft}=f_s$, which never really happens, you can't read correct peak amplitudes and the noise spectral density at the same time. You either plot two curves, of compute it manually.

In $\text{dBW}$, one handy way to go back and forth normalized and unnormalized spectrums is to respectively add or substract $10\log_{10}(\text{nfft}) - 10\log_{10}(fs)$.

Actually, dedicated hardware (Spectral Analyzers) often offer a switch button to display either the Power Spectrum in $\text{dBm}$ or Power Spectrum Density $\text{dBm/Hz}$. The two terms seem to be used interchangeably in the documentation / literature. People will often mean the same thing using both words, so be careful. 

I hope this subject was made a little bit clearer, and see you next time !