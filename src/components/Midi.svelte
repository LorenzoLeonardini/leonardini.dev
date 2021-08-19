<script>
	import { onMount } from 'svelte';
	let midi_devices = [];
	let midi_events = [];
	const notes = [ 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B' ];

	let audioContext;
	const oscList = {};
	let mainGainNode = null;

	function decodeMIDI(message) {
		// velocity might not be included
		if(message.data.length === 2) message.data.length.push(127);

		const [command, note, velocity] = message.data;
		const octave = Math.floor((note - 60 + (4 * 12)) / 12);
		const note_name = notes[((note % 12) + 12) % 12];

		let string = '';
		let channel;
		if((command & 0x90) === 0x90) {
			string += 'Note ON';
			channel = command - 0x90;

			let gainNode = audioContext.createGain();
			gainNode.connect(mainGainNode);
			gainNode.gain.value = velocity / 127;

			let osc = audioContext.createOscillator();
			osc.connect(gainNode);
			osc.type = 'triangle';

			osc.frequency.value = 440 * Math.pow(2, (note - 69) / 12);
			console.log(osc.frequency.value);
			oscList[note] = osc;
			osc.start();
		} else if((command & 0x80) === 0x80) {
			string += 'Note OFF';
			channel = command - 0x80;
			oscList[note].stop();
			oscList[note] = null;
		}
		string += ' on channel ' + channel;
		string += ': ' + note_name + octave;
		string += ', velocity: ' + velocity;
		return string;
	}

	let imported = false;
	function setUp() {
		if(navigator.requestMIDIAccess) {
			console.log('Browser supports WebMIDI');
			navigator.requestMIDIAccess().then((midiAccess) => {
				const inputs = midiAccess.inputs;
				for(let input of inputs.values()) {
					midi_devices = [...midi_devices, input.name];
					input.onmidimessage = function(message) {
						midi_events = [decodeMIDI(message)];
						// console.log(message);
					}
				}
			}).catch((err) => {
				console.error(err);
			})
		} else {
			console.log('WebMIDI not supported on this browser');
			if(!imported) {
				import('/WebMIDIAPI.min.js').then(module => {
					imported = true;
					setUp();
				});
			}
		}


		audioContext = new (window.AudioContext || window.webkitAudioContext)();
		mainGainNode = audioContext.createGain();
  		mainGainNode.connect(audioContext.destination);
		mainGainNode.gain.value = .8;
	}

	onMount(setUp)
</script>

<style lang="scss">
	main h1 {
		text-align: center;
		margin: .6em;
	}
</style>

<main>
	<h1>Input MIDI Devices:</h1>

	<div>
		<ul>
			{#each midi_devices as device}
				<li>{device}</li>
			{/each}
		</ul>
	</div>

	<h1>MIDI events:</h1>

	<div>
		{#each midi_events as event}
			<pre>
				{JSON.stringify(event)}
			</pre>
		{/each}
	</div>
</main>