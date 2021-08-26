<script lang="ts">
	import { onMount } from 'svelte';

	let playing = false;
	let wavesurfer;
	let small = false;

	function togglePlay() {
		if(playing) {
			wavesurfer.pause();
		} else {
			wavesurfer.play();
		}
		playing = !playing;
	}

	onMount(() => {
		const library = document.createElement('script');
		library.src = 'https://unpkg.com/wavesurfer.js@5.2.0/dist/wavesurfer.min.js';

		library.addEventListener('load', () => {
			wavesurfer = (window as any).WaveSurfer.create({
				container: '#waveform',
				waveColor: '#f0f0f0',
				progressColor: '#DF99F0',
				height: 70,
				barWidth: 2
			});
			wavesurfer.load('/assets/alone_in_space.mp3')
		});
		document.body.appendChild(library);

		const observer = new IntersectionObserver(
			(entries, observer) => {
				entries.forEach(entry => {
					small = entry.boundingClientRect.y < 0;
				});
			}, {
				threshold: [1]
			}
		);
		observer.observe(document.querySelector('.sticky'));
	})
</script>

<style lang="scss">
	.player-container {
		background: var(--darker-blue);
		--height: 150px;
		--transition-time: .15s;
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
				opacity: .8;
				border: solid 3px var(--light);
				cursor: pointer;
				opacity: 0;
				transition: opacity .1s ease,
						transform var(--transition-time) ease;

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

						&::before, &::after {
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

			.song-name, .song-artist {
				display: inline-block;
				position: absolute;
				color: var(--light);
				left: var(--height);
				margin-left: 1rem;
				top: .7em;
			}

			.song-name {
				font-size: 1.2em;
				font-weight: bold;
			}

			.song-artist {
				margin-top: 2em;
				opacity: .8;
				font-size: .9em;
			}
			
			.waveform-container {
				position: absolute;
				bottom: 10px;
				left: calc(var(--height) + 2em);
				right: 2em;
			}
		}

		&.small {
			transform: scale(1, .6);

			.album-cover { transform: scaleX(.6); }
			.play-button { transform: scaleX(.6) translate(-16px, 1px); }
			.song-name { transform: scale(.69, 1.2) translate(-82px, -2px); }

			.song-artist {
				transform: scale(.8, 1.35) translate(10ch, calc(-2px - 1.15em));

				&::before {
					content: '-';
					position: absolute;
					left: -15px;
				}
			}
			
			.waveform-container { transform: scale(1, 1.17) translate(-70px, -.8em); }
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
	.song-artist,
	.waveform-container {
		transition: transform var(--transition-time) ease;
		transform-origin: top left;
	}

	@media (prefers-reduced-motion) {
		.player-container {
			--transition-time: 0s;
		}
	}
</style>

<div class="player-container" class:small={small}>
	<div class="container-fluid">
		<img src="/assets/alone_in_space.jpg" alt="Alone in Space album cover" class="album-cover" width="150" height="150">
		<div class="play-button" on:click={togglePlay}>
			<div class="play-icon" class:pause={playing}></div>
		</div>
		<div class="song-name">Alone in Space</div>
		<div class="song-artist">Lorenzo Leonardini</div>
		<div class="waveform-container">
			<div id="waveform"></div>
		</div>
	</div>
</div>