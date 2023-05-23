<script lang="ts">
	import { onMount } from 'svelte'

	let waveform: Array<number>
	let canvas: HTMLCanvasElement
	let width: number, height: number
	let audio: HTMLAudioElement

	let playing = false
	let small = false

	function togglePlay() {
		if (playing) {
			audio.pause()
		} else {
			audio.play()
		}
		playing = !playing
	}

	const resizeHandler = () => {
		canvas.width = Math.floor(canvas.clientWidth * window.devicePixelRatio)
		canvas.height = Math.floor(canvas.clientHeight * window.devicePixelRatio)
		width = canvas.width
		height = canvas.height

		draw()
	}

	const normalize = (array: Array<number>) => {
		const max = Math.max(...array)
		for (let i = 0; i < array.length; i++) {
			array[i] /= max
		}
	}

	const draw = () => {
		const ctx = canvas.getContext('2d')
		ctx.clearRect(0, 0, width, height)

		const bar_width = 2 * window.devicePixelRatio
		const bar_space = 1 * window.devicePixelRatio

		const amount = Math.floor(width / (bar_width + bar_space))
		let wave = []
		const samples = Math.floor(waveform.length / amount)
		for (let i = 0; i < amount; i++) {
			let avg = 0
			for (let j = 0; j < samples; j++) {
				avg += waveform[i * samples + j]
			}
			wave.push(avg)
		}

		normalize(wave)
		wave = wave.map((e) => e + Math.pow(10, 1 + e))
		normalize(wave)

		let not_played = 0
		if (audio && audio.currentTime && audio.duration) {
			not_played = Math.ceil((amount * audio.currentTime) / audio.duration)
		}

		const scale = 1.5

		ctx.fillStyle = `#DD90F0`
		for (let i = 0; i < not_played; i++) {
			ctx.fillRect(
				i * (bar_width + bar_space),
				(height - (wave[i] * height) / scale) / 2,
				bar_width,
				(wave[i] * height) / scale
			)
		}

		ctx.fillStyle = `rgba(240,240,240,0.8)`
		for (let i = not_played; i < amount; i++) {
			ctx.fillRect(
				i * (bar_width + bar_space),
				(height - (wave[i] * height) / scale) / 2,
				bar_width,
				(wave[i] * height) / scale
			)
		}

		ctx.strokeStyle = `rgba(240,240,240,.6)`
		ctx.beginPath()
		ctx.moveTo((width * audio.currentTime) / audio.duration, 0)
		ctx.lineTo((width * audio.currentTime) / audio.duration, height)
		ctx.stroke()
	}

	onMount(async () => {
		waveform = await fetch('/assets/alone_in_space.json').then((data) => data.json())

		document.body.onresize = resizeHandler
		resizeHandler()

		audio.ontimeupdate = () => {
			draw()
		}

		canvas.onclick = (e: PointerEvent) => {
			if (!audio) return
			const position = ((e as any).layerX + (small ? 60 : 0)) * window.devicePixelRatio
			const seek = (position / (width + (small ? 60 : 0))) * audio.duration
			audio.currentTime = Math.floor(seek)
		}

		const observer = new IntersectionObserver(
			(entries, observer) => {
				entries.forEach((entry) => {
					small = entry.boundingClientRect.y < 0
				})
			},
			{
				threshold: [1]
			}
		)
		observer.observe(document.querySelector('.sticky'))
	})
</script>

<style lang="scss">
	.player-container {
		background: var(--darker-blue);
		--height: 150px;
		--transition-time: 0.15s;
		font-family: var(--sans-serif);

		.container-fluid {
			display: block;
			position: relative;

			.album-cover {
				height: var(--height);
				display: block;
			}

			.play-button {
				--size: calc(calc(var(--height) * 2) / 3);
				width: var(--size);
				height: var(--size);
				position: absolute;
				top: calc(calc(var(--height) - var(--size)) / 2);
				left: calc(calc(var(--height) - var(--size)) / 2);
				background: var(--darker-blue);
				border-radius: 50%;
				opacity: 0.8;
				border: solid 3px var(--light);
				cursor: pointer;
				opacity: 0;
				transition: opacity 0.1s ease, transform var(--transition-time) ease;

				.play-icon {
					width: 30px;
					height: 20px;
					border: solid 20px transparent;
					border-left: solid 30px var(--light);
					position: absolute;
					top: 50%;
					left: 50%;
					transform: translate(-20%, -50%);

					&.pause {
						border-left: solid 30px transparent;
						transform: translate(0, 0);

						&::before,
						&::after {
							content: '';
							position: absolute;
							top: -40px;
							left: -44px;
							width: 10px;
							height: 40px;
							background: var(--light);
						}

						&::after {
							left: -24px;
						}
					}
				}

				&:hover {
					background: #404040;
				}
			}

			.song-name,
			.song-artist {
				display: inline-block;
				position: absolute;
				color: var(--light);
				left: var(--height);
				margin-left: 1rem;
				top: 0.7em;
			}

			.song-name {
				font-size: 1.2em;
				font-weight: bold;
			}

			.song-artist {
				margin-top: 2em;
				opacity: 0.8;
				font-size: 0.9em;
			}

			.waveform-container {
				position: absolute;
				bottom: 10px;
				left: calc(var(--height) + 2em);
				right: 2em;
				height: 70px;
				transition: transform var(--transition-time) ease, right var(--transition-time) ease;

				canvas {
					width: 100%;
					height: 100%;
				}
			}
		}

		&.small {
			transform: scale(1, 0.6);

			.album-cover {
				transform: scaleX(0.6);
			}
			.play-button {
				transform: scaleX(0.6) translate(-16px, 1px);
			}
			.song-name {
				transform: scale(0.69, 1.2) translate(-82px, -2px);
			}

			.song-artist {
				transform: scale(0.8, 1.35) translate(10ch, calc(-2px - 1.15em));

				&::before {
					content: '-';
					position: absolute;
					left: -15px;
				}
			}

			.waveform-container {
				transform: scale(1, 1.17) translate(-60px, -0.8em);
				right: calc(2em - 60px);
			}
		}

		&:hover {
			.play-button {
				opacity: 1;
			}
		}
	}

	.player-container,
	.album-cover,
	.play-button,
	.song-name,
	.song-artist {
		transition: transform var(--transition-time) ease;
		transform-origin: top left;
	}

	@media (prefers-reduced-motion) {
		.player-container {
			--transition-time: 0s;
		}
	}
</style>

<div class="player-container" class:small="{small}">
	<div class="container-fluid">
		<img
			src="/assets/alone_in_space.webp"
			alt="Alone in Space album cover"
			class="album-cover"
			width="150"
			height="150" />
		<div class="play-button" on:click="{togglePlay}">
			<div class="play-icon" class:pause="{playing}"></div>
		</div>
		<div class="song-name">Alone in Space</div>
		<div class="song-artist">Lorenzo Leonardini</div>
		<div class="waveform-container">
			<canvas bind:this="{canvas}"></canvas>
		</div>
		<audio bind:this="{audio}">
			<source src="/assets/alone_in_space.mp3" type="audio/mp3" />
		</audio>
	</div>
</div>
