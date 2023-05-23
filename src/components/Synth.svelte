<script lang="ts">
	import { onMount } from 'svelte'

	const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
	const _12th_root = Math.pow(2, 1 / 12)

	let midi_devices: Array<WebMidi.MIDIInput> = []
	let midi_channel: number = -1
	let midi_device: WebMidi.MIDIInput = null
	let old_midi_device: WebMidi.MIDIInput
	let midi_enabled = true
	let midiAccess: WebMidi.MIDIAccess = null

	$: {
		if (old_midi_device != null) {
			old_midi_device.onmidimessage = null
		}
		if (midi_device) {
			old_midi_device = midi_device
			midi_device.onmidimessage = decodeMIDI
		}
	}

	$: {
		if (audio.filter != null) {
			audio.filter.frequency.value = 40 + ktv(knobs.cutoff.rotation) * 20000
			audio.filter.Q.value = ktv(knobs.resonance.rotation) * 50 + 1
		}
	}

	let imported = false

	const audio: {
		context: AudioContext
		masterVolume: GainNode
		filter: BiquadFilterNode
		lfo: OscillatorNode
		lfoGain: GainNode
		oscillators: {
			[note: string]: {
				gain: GainNode
				saw_gain: GainNode
				triangle_gain: GainNode
				saw: OscillatorNode
				triangle: OscillatorNode
				playing: boolean
			}
		}
	} = {
		context: null,
		masterVolume: null,
		filter: null,
		lfo: null,
		lfoGain: null,
		oscillators: {}
	}

	// Knob to value
	const ktv = (value: number) => (value + 132) / 264

	function decodeMIDI(message) {
		const command = message.data[0]
		const note = message.data[1]
		const octave = Math.floor((note - 60 + 4 * 12) / 12)
		const note_name = notes[((note % 12) + 12) % 12]

		let channel: number
		if (command >> 4 === 0x9) {
			channel = command - 0x90
			if (midi_channel !== -1 && midi_channel !== channel) {
				return
			}
			playNote(note_name + octave)
		} else if (command >> 4 === 0x8) {
			channel = command - 0x80
			if (midi_channel !== -1 && midi_channel !== channel) {
				return
			}
			stopNote(note_name + octave)
		} else if (command >> 4 === 0xb) {
			channel = command - 0xb0
			if (midi_channel !== -1 && midi_channel !== channel) {
				return
			}
			const value = message.data[2]
			audio.lfoGain.gain.value = (value * 10) / 127
		}
	}

	function playNote(note: string): void {
		if (audio.context == null) {
			setupAudioContext()
		}

		if (!(note in audio.oscillators)) {
			const octave = parseInt(note[note.length - 1])
			const idx = notes.indexOf(note.substr(0, note.length - 1))
			const position = idx + 12 * octave
			const frequency = 440 * Math.pow(_12th_root, position - (9 + 12 * 4))

			const gain = audio.context.createGain()
			const saw = audio.context.createGain()
			const triangle = audio.context.createGain()

			const saw_oscillator = audio.context.createOscillator()
			saw_oscillator.frequency.setValueAtTime(frequency, 0)
			audio.lfoGain.connect(saw_oscillator.frequency)
			saw_oscillator.type = 'sawtooth'

			const triangle_oscillator = audio.context.createOscillator()
			triangle_oscillator.frequency.setValueAtTime(frequency, 0)
			audio.lfoGain.connect(triangle_oscillator.frequency)
			triangle_oscillator.type = 'triangle'

			saw_oscillator.connect(saw)
			saw_oscillator.start()

			triangle_oscillator.connect(triangle)
			triangle_oscillator.start()

			saw.connect(gain)
			triangle.connect(gain)

			gain.connect(audio.masterVolume)

			audio.oscillators[note] = {
				gain: gain,
				triangle_gain: triangle,
				triangle: triangle_oscillator,
				saw_gain: saw,
				saw: saw_oscillator,
				playing: true
			}
		}

		const sustainLevel = ktv(knobs.sustain.rotation)
		const attackTime = ktv(knobs.attack.rotation) + 0.01
		const decayTime = ktv(knobs.decay.rotation) + 0.01
		const sawLevel = ktv(knobs.saw.rotation)
		const triangleLevel = ktv(knobs.triangle.rotation)

		audio.oscillators[note].triangle_gain.gain.value = triangleLevel
		audio.oscillators[note].saw_gain.gain.value = sawLevel

		audio.oscillators[note].gain.gain.cancelScheduledValues(audio.context.currentTime)
		audio.oscillators[note].gain.gain.value = 0
		audio.oscillators[note].gain.gain.linearRampToValueAtTime(
			sustainLevel,
			audio.context.currentTime + attackTime
		)
		audio.oscillators[note].gain.gain.linearRampToValueAtTime(
			sustainLevel - 0.05,
			audio.context.currentTime + attackTime + decayTime
		)

		audio.oscillators[note].playing = true
	}

	function stopNote(note: string): void {
		if (!(note in audio.oscillators)) {
			return
		}

		const releaseTime = ktv(knobs.release.rotation) + 0.01
		const gain = audio.oscillators[note].gain
		const current_gain = gain.gain.value
		audio.oscillators[note].gain.gain.cancelScheduledValues(audio.context.currentTime)
		gain.gain.setValueAtTime(current_gain, audio.context.currentTime)
		gain.gain.linearRampToValueAtTime(0, audio.context.currentTime + releaseTime)
		audio.oscillators[note].playing = false
	}

	function findDevices(): void {
		midi_devices = []
		const inputs = midiAccess.inputs
		for (let input of inputs.values()) {
			midi_devices = [...midi_devices, input]
		}
		if (midi_devices.length > 0) {
			midi_device = midi_devices[0]
		}
	}

	function setupAudioContext() {
		if (audio.context != null) return

		const AudioContext = window.AudioContext || (window as any).webkitAudioContext
		audio.context = new AudioContext()

		// Master volume
		audio.masterVolume = audio.context.createGain()

		// Filter
		audio.filter = audio.context.createBiquadFilter()
		audio.filter.type = 'lowpass'
		audio.filter.frequency.value = 40 + ktv(knobs.cutoff.rotation) * 20000
		audio.filter.Q.value = ktv(knobs.resonance.rotation) * 50 + 1

		audio.masterVolume.connect(audio.filter)
		audio.filter.connect(audio.context.destination)

		audio.lfoGain = audio.context.createGain()
		audio.lfoGain.gain.value = 0

		audio.lfo = audio.context.createOscillator()
		audio.lfo.type = 'sine'
		audio.lfo.frequency.setValueAtTime(10, 0)
		audio.lfo.connect(audio.lfoGain)
		audio.lfo.start()
	}

	function setUp() {
		/* ------------ Setting up MIDI ------------ */
		if (navigator.requestMIDIAccess) {
			console.log('Browser supports WebMIDI')
			navigator
				.requestMIDIAccess()
				.then((_midiAccess) => {
					midiAccess = _midiAccess
					findDevices()
				})
				.catch((err) => {
					console.log('Nevermind.')
					console.error(err)
					midi_enabled = false
				})
		} else {
			console.log('WebMIDI not supported on this browser')
			if (!imported) {
				// @ts-ignore: import generates error for no reason
				require('/WebMIDIAPI.min.js')
					.then((module) => {
						imported = true
						setUp()
					})
					.catch(() => {
						midi_enabled = false
					})
			}
		}
		/* ------------ Setting up audio context ------------ */
		document.body.onclick = setupAudioContext
		document.body.ontouchstart = setupAudioContext

		/* ------------ Rotating knobs ------------ */
		for (let id in knobs) {
			const knob: HTMLElement = document.querySelector(`.knob[data-id="${id}"]`)
			knob.style.transform = `rotate(${knobs[id].rotation}deg)`
		}
	}

	onMount(setUp)

	const knobs: {
		[id: string]: {
			label: string
			rotation: number
		}
	} = {
		saw: {
			label: 'Saw',
			rotation: -100
		},
		triangle: {
			label: 'Triang',
			rotation: -132
		},
		cutoff: {
			label: 'Cutoff',
			rotation: -66
		},
		resonance: {
			label: 'Reson.',
			rotation: -132
		},
		attack: {
			label: 'Attack',
			rotation: -132
		},
		decay: {
			label: 'Decay',
			rotation: -132
		},
		sustain: {
			label: 'Sustain',
			rotation: 0
		},
		release: {
			label: 'Release',
			rotation: -132
		}
	}

	function rotateKnob(knob_id: string, y: number, element: HTMLElement) {
		if (knob_id == null) return
		// Knob Rotation
		if (y - currentY !== 0) {
			knobs[knob_id].rotation -= (y - currentY) * 4
		}
		currentY = y

		// Setting Max rotation
		if (knobs[knob_id].rotation >= 132) {
			knobs[knob_id].rotation = 132
		} else if (knobs[knob_id].rotation <= -132) {
			knobs[knob_id].rotation = -132
		}

		element.style.transform = `rotate(${knobs[knob_id].rotation}deg)`
	}

	let currentY = 0
	function knobMouseDrag(mousemove) {
		if (mousemove.buttons !== 1) {
			return
		}

		const knob_id = mousemove.target.dataset.id
		rotateKnob(knob_id, mousemove.pageY, mousemove.target)
	}

	function knobTapDrag(touchmove) {
		console.log(touchmove)

		const knob_id = touchmove.target.dataset.id
		rotateKnob(knob_id, touchmove.touches[0].pageY, touchmove.target)
		// rotateKnob(knob_id, mousemove.pageY, mousemove.target);
	}
</script>

<style lang="scss">
	@import url('https://fonts.googleapis.com/css2?family=Satisfy&display=swap');

	@keyframes rotation {
		0% {
			transform: rotate(-180deg) translateY(2px);
		}
		100% {
			transform: rotate(0deg) translateY(2px);
		}
	}

	.hidden {
		display: none;
	}

	.keyboard-container {
		width: auto;
		background: var(--darker-blue);
		padding: 50px 0 70px 0;
		text-align: center;
		position: relative;
		z-index: 999;
	}

	.keyboard {
		height: 200px;
		position: relative;
		display: inline-block;
		width: auto;
		background: var(--dark-blue);
		padding: 40px 20px 20px 20px;
		border-radius: 6px;
		border: solid 1px var(--dark-blue-lighter);
	}

	.logo {
		position: absolute;
		color: rgba(255, 255, 255, 0.8);
		top: 6px;
		right: 50px;
		font-size: 0.7em;
		font-family: monospace;

		.cursive {
			font-family: 'Satisfy', cursive;
			font-size: 1.2rem;
			margin-right: 6px;
		}
	}

	.midi,
	.nomidi {
		position: absolute;
		left: 20px;
		color: rgba(255, 255, 255, 0.8);
		font-family: monospace;
		top: 9px;
		font-size: 0.8em;
	}

	.nomidi {
		color: var(--red);
		top: 12px;
	}

	.reload-button {
		display: inline-block;
		transform: translateY(2px);
		cursor: pointer;

		&:hover {
			animation: rotation 0.4s linear;
		}
	}

	.controls {
		display: inline-block;
		height: 100%;
		margin-right: 20px;
		width: calc(54px * 4);
		transform: translateY(-13px);

		&,
		* {
			-webkit-user-drag: none;
			-khtml-user-drag: none;
			-moz-user-drag: none;
			-o-user-drag: none;
		}
	}

	.knob-container {
		display: inline-block;
		position: relative;
		margin: 13px 0;

		.label {
			display: inline-block;
			position: absolute;
			bottom: 0px;
			font-size: 0.6em;
			color: white;
			font-family: monospace;
			left: 50%;
			transform: translateX(-50%);
			white-space: nowrap;
			-webkit-touch-callout: none; /* iOS Safari */
			-webkit-user-select: none; /* Safari */
			-khtml-user-select: none; /* Konqueror HTML */
			-moz-user-select: none; /* Old versions of Firefox */
			-ms-user-select: none; /* Internet Explorer/Edge */
			user-select: none;
		}
	}

	.knob {
		width: 30px;
		height: 30px;
		border-radius: 50%;
		background: var(--blue);
		display: inline-block;
		margin: 0 12px 10px 12px;
		position: relative;
		cursor: pointer;

		&::after {
			content: '';
			display: block;
			position: absolute;
			width: 2px;
			height: 10px;
			background: rgba(255, 255, 255, 0.8);
			left: 50%;
			transform: translateX(-50%);
		}
	}

	.keys-container {
		display: inline-block;
		position: relative;
		height: 100%;
	}

	.key {
		display: inline-block;
		margin: 0;
		border-bottom-left-radius: 2px;
		border-bottom-right-radius: 2px;
		cursor: pointer;
		margin-left: 2px;
		box-shadow: inset 0px 8px 10px -8px #000000;

		&:not(.key + .key) {
			box-shadow: inset 8px 8px 10px -8px #000000;
		}

		&.white {
			background: #ffffff;
			width: 30px;
			height: 100%;
			&:hover {
				background: #e5e5e5;
			}
			&:active,
			&.active {
				background: #b0b0b0;
			}
		}

		&.black {
			background: black;
			width: 20px;
			height: 60%;
			position: absolute;
			transform: translateX(-50%);

			&:hover {
				background: #151515;
			}

			&:active,
			&.active {
				background: #303030;
			}
		}
	}

	.depth {
		position: absolute;
		top: 20px;
		left: 10px;
		right: -10px;
		bottom: -20px;
		z-index: -2;
		background: #0c1217;
		border-radius: 6px;
		border: solid 1px #0c1217;
		box-shadow: 3px 3px 16px 1px #000000;

		&::before,
		&::after {
			content: '';
			position: absolute;
			z-index: -1;
			border-radius: 6px;
			background: #0c1217;
		}

		&::before {
			bottom: 3px;
			left: -7px;

			width: 30px;
			height: 28px;

			transform: rotate(-27deg);
		}

		&::after {
			top: -18px;
			right: 3px;

			width: 30px;
			height: 33px;

			transform: rotate(-23deg);
		}
	}

	select {
		appearance: none;
		background-color: transparent;
		border: none;
		margin: 0;
		font-family: inherit;
		font-size: inherit;
		cursor: inherit;
		line-height: inherit;
		/* outline: none; */
		color: white;
		background: var(--dark-blue-lighter);
		border: solid 1px var(--blue);
		border-radius: 3px;
		padding: 0.15em 1.3em 0.15em 0.4em;
		cursor: pointer;
	}

	.select {
		display: inline-block;
		position: relative;

		&::after {
			content: '';
			position: absolute;
			top: 8px;
			right: 6px;
			width: 0.7em;
			height: 0.4em;
			background-color: var(--blue);
			clip-path: polygon(100% 0%, 0 0%, 50% 100%);
		}
	}

	@media screen and (max-width: 700px) {
		.keyboard-container {
			padding: 0;
		}

		.keyboard {
			height: 270px;
			width: 100%;
			padding: 40px 10px 20px 10px;
		}

		.controls {
			width: calc(54px * 8);
			transform: translateY(-4px);
			margin-right: 0;
			height: auto;
		}

		.keys-container {
			height: 138px;
		}

		.depth {
			display: none;
		}
	}

	@media screen and (max-width: 700px) and (orientation: portrait) {
		.controls {
			width: calc(54px * 5);
		}

		.knob-container[data-id='resonance'],
		.knob-container[data-id='triangle'],
		.knob-container[data-id='decay'],
		.portrait-hidden,
		.midi {
			display: none;
		}
	}
</style>

<div class="keyboard-container">
	<div class="keyboard">
		<div class="logo"><span class="cursive">Leo</span> digital synth</div>
		<div class="nomidi" class:hidden="{midi_enabled}">This browser does not support midi</div>
		<div class="midi" class:hidden="{!midi_enabled}">
			Midi device:
			<div class="select" on:select="{console.log}">
				<select bind:value="{midi_device}">
					{#if midi_devices.length === 0}
						<option disabled selected>No device</option>
					{/if}
					{#each midi_devices as device, idx}
						<option value="{device}">{device.name}</option>
					{/each}
				</select>
			</div>
			<div class="select">
				<select bind:value="{midi_channel}">
					<option value="{-1}">Ch all</option>
					{#each [...Array(16).keys()] as i}
						<option value="{i}">Ch {i + 1}</option>
					{/each}
				</select>
			</div>
			<div
				on:click="{findDevices}"
				class="reload-button"
				title="Reload devices"
				alt="Reload devices">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="16"
					height="16"
					fill="currentColor"
					class="bi bi-arrow-repeat"
					viewBox="0 0 16 16">
					<path
						d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41zm-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9z"
					></path>
					<path
						fill-rule="evenodd"
						d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5.002 5.002 0 0 0 8 3zM3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9H3.1z"
					></path>
				</svg>
			</div>
		</div>
		<div class="controls">
			{#each Object.keys(knobs) as idx}
				<div class="knob-container" data-id="{idx}">
					<div
						on:mousedown="{(event) => {
							currentY = event.pageY
						}}"
						on:touchstart="{(event) => {
							currentY = event.touches[0].pageY
						}}"
						on:mousemove|preventDefault="{knobMouseDrag}"
						on:touchmove|preventDefault="{knobTapDrag}"
						class="knob"
						data-id="{idx}">
					</div>
					<div class="label">{knobs[idx].label}</div>
				</div>
			{/each}
		</div>
		<div class="keys-container">
			{#each [...Array(3).keys()] as octave}
				{#each notes as note}
					<div
						class="key"
						class:white="{!note.endsWith('#')}"
						class:black="{note.endsWith('#')}"
						class:active="{`${note}${octave + 3}` in audio.oscillators &&
							audio.oscillators[`${note}${octave + 3}`].playing}"
						class:portrait-hidden="{octave !== 0 && !(octave === 1 && notes.indexOf(note) < 5)}"
						class:mobile-hidden="{octave === 2}"
						on:mousedown="{() => playNote(`${note}${octave + 3}`)}"
						on:touchstart|preventDefault="{() => playNote(`${note}${octave + 3}`)}"
						on:mouseup="{() => stopNote(`${note}${octave + 3}`)}"
						on:touchend|preventDefault="{() => stopNote(`${note}${octave + 3}`)}"
						on:mouseleave="{() => stopNote(`${note}${octave + 3}`)}"
						on:touchcancel|preventDefault="{() => stopNote(`${note}${octave + 3}`)}"
						id="{note}{octave + 3}">
					</div>
				{/each}
			{/each}
		</div>
		<div class="depth"></div>
	</div>
</div>
