<script>
	import { onMount } from 'svelte';

	const notes = [ 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B' ];

	let midi_devices = [];
	let midi_enabled = true;
	let midiAccess = null

	let imported = false;

	function findDevices() {
		midi_devices = [];
		const inputs = midiAccess.inputs;
		for(let input of inputs.values()) {
			midi_devices = [...midi_devices, input.name];
		}
	}

	function setUp() {
		if(navigator.requestMIDIAccess) {
			console.log('Browser supports WebMIDI');
			navigator.requestMIDIAccess().then((_midiAccess) => {
				midiAccess = _midiAccess;
				findDevices();
			}).catch((err) => {
				console.log('Nevermind.')
				console.error(err);
				midi_enabled = false;
			})
		} else {
			console.log('WebMIDI not supported on this browser');
			if(!imported) {
				import('/WebMIDIAPI.min.js').then(module => {
					imported = true;
					setUp();
				}).catch(() => {
					midi_enabled = false;
				});
			}
		}
	}

	onMount(setUp);

	const knobs = [
		{
			label: 'Saw',
			rotation: -132
		},
		{
			label: 'Triang',
			rotation: -132
		},
		{
			label: 'Cutoff',
			rotation: -132
		},
		{
			label: 'Reson.',
			rotation: -132
		},
		{
			label: 'Attack',
			rotation: -132
		},
		{
			label: 'Decay',
			rotation: -132
		},
		{
			label: 'Sustain',
			rotation: -132
		},
		{
			label: 'Release',
			rotation: -132
		}
	]

	let currentY = 0;
	function movingKnob(mousemove) {
		if(mousemove.buttons !== 1) {
			return;
		}

		const knob_id = parseInt(mousemove.target.dataset.id);
		if(knob_id == null || isNaN(knob_id)) return;
		// Knob Rotation
		if(mousemove.pageY - currentY !== 0) { 
			knobs[knob_id].rotation -= (mousemove.pageY - currentY) * 4;
		}
		currentY = mousemove.pageY;

		// Setting Max rotation
		if(knobs[knob_id].rotation >= 132) { knobs[knob_id].rotation = 132; } 
		else if(knobs[knob_id].rotation <= -132) { knobs[knob_id].rotation = -132; }

		mousemove.target.style.transform=`rotate(${knobs[knob_id].rotation}deg)`;
	}
</script>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Satisfy&display=swap');
	
	.keyboard-container {
		height: 320px;
		width: auto;
		background: var(--dark);
		padding: 50px 0;
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

	.key {
		display:inline-block;
		margin: 0;
		border-bottom-left-radius: 2px;
		border-bottom-right-radius: 2px;
		cursor: pointer;
		margin-left: 2px;
		box-shadow: inset 0px 8px 10px -8px #000000;
	}

	.key:not(.key + .key) {
		box-shadow: inset 8px 8px 10px -8px #000000;
	}

	.key.white {
		background: white;
		width: 30px;
		height: 100%;
	}

	.key.white:hover {
		background: #e5e5e5;
	}
	.key.white:active {
		background: #b0b0b0;
	}

	.key.black {
		background: black;
		width: 20px;
		height: 60%;
		position: absolute;
		transform: translateX(-50%);
	}

	.key.black:hover {
		background: #151515;
	}
	.key.black:active {
		background: #303030;
	}

	.logo {
		position: absolute;
		color: rgba(255, 255, 255, .8);
		top: 6px;
		right: 50px;
		font-size: .7em;
		font-family: monospace;
	}

	.logo .cursive {
		font-family: 'Satisfy', cursive;
		font-size: 1.2rem;
		margin-right: 6px;
	}

	.controls {
		display: inline-block;
		height: 100%;
		margin-right: 20px;
		width: calc(54px * 4);
		transform: translateY(-13px);
	}

	.knob-container {
		display: inline-block;
		position: relative;
		margin: 13px 0;
	}

	.knob {
		width: 30px;
		height: 30px;
		border-radius: 50%;
		background: var(--blue);
		display: inline-block;
		margin: 0 12px 10px 12px;
		position: relative;
		transform: rotate(-132deg);
		cursor: pointer;
	}

	.knob::after {
		content: '';
		display: block;
		position: absolute;
		width: 2px;
		height: 10px;
		background: rgba(255, 255, 255, .8);
		left: 50%;
		transform: translateX(-50%);
	}

	.knob-container .label {
		display: inline-block;
		position: absolute;
		bottom: 0px;
		font-size: .6em;
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

	.midi, .nomidi {
		position: absolute;
		left: 20px;
		color: rgba(255, 255, 255, .8);
		font-family: monospace;
		top: 9px;
		font-size: .8em;
	}

	.nomidi {
		color: var(--red);
		top: 12px;
	}

	.reload-button {
		display: inline-block;
		transform: translateY(2px);
		cursor: pointer;
	}

	.reload-button:hover {
		animation: rotation .4s linear;
	}

	@keyframes rotation {
		0% {
			transform: rotate(-180deg) translateY(2px);
		}
		100% {
			transform: rotate(0deg) translateY(2px);
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
		padding: .15em 1.3em .15em .4em;
		cursor: pointer;
	}

	.select {
		display: inline-block;
		position: relative;
	}

	.select::after {
		content: '';
		position: absolute;
		top: 8px;
		right: 6px;
		width: 0.7em;
		height: 0.4em;
		background-color: var(--blue);
		clip-path: polygon(100% 0%, 0 0%, 50% 100%);
	}

	.keys-container {
		display: inline-block;
		position: relative;
		height: 100%;
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
	}

	.depth::before {
		content: '';
		position: absolute;
		bottom: 3px;
		left: -7px;
		width: 30px;
		height: 28px;
		z-index: -1;
		border-radius: 6px;
		background: #0c1217;
		transform: rotate(-27deg);
	}

	.depth::after {
		content: '';
		position: absolute;
		top: -18px;
		right: 3px;
		width: 30px;
		height: 33px;
		z-index: -1;
		border-radius: 6px;
		background: #0c1217;
		transform: rotate(-23deg);
	}

	.hidden {
		display: none;
	}
</style>

<div class="keyboard-container">
	<div class="keyboard">
		<div class="logo"><span class="cursive">Leo</span> digital synth</div>
		<div class="nomidi" class:hidden={midi_enabled}>This browser does not support midi</div>
		<div class="midi" class:hidden={!midi_enabled}>
			Midi device: 
			<div class="select" on:select={console.log}>
				<select>
					{#if midi_devices.length === 0}
						<option disabled selected>No device</option>
					{/if}
					{#each midi_devices as device}
						<option value={device}>{device}</option>
					{/each}
				</select>
			</div>
			<div class="select">
				<select>
					<option value="-1">Ch all</option>
					{#each [...Array(16).keys()] as i}
						<option value={i}>Ch {i + 1}</option>
					{/each}
				</select>
			</div>
			<div on:click={findDevices} class="reload-button" title="Reload devices" alt="Reload devices">
				<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-repeat" viewBox="0 0 16 16">
					<path d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41zm-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9z"/>
					<path fill-rule="evenodd" d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5.002 5.002 0 0 0 8 3zM3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9H3.1z"/>
				</svg>
			</div>
		</div>
		<div class="controls">
			{#each knobs as knob, idx}
				<div class="knob-container">
					<div on:mousedown={(event) => {currentY = event.pageY}} on:mousemove={movingKnob} class="knob" data-id="{idx}"></div>
					<div class="label">{knob.label}</div>
				</div>
			{/each}
		</div>
		<div class="keys-container">
			{#each [...Array(3).keys()]  as octave}
				{#each notes as note}
					<div class="key"
						class:white={!note.endsWith('#')}
						class:black={note.endsWith('#')}
						class:mobile-hidden={octave === 2}
						id="{note}{octave + 3}"></div>
				{/each}
			{/each}
		</div>
		<div class="depth"></div>
	</div>
</div>