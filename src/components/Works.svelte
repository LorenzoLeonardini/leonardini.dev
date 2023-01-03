<script lang="ts">
	import Lazyload from './Lazyload.svelte'
</script>

<style lang="scss">
	h2 {
		margin-bottom: 1em;
		text-align: left;
	}

	.left {
		text-align: right;
	}

	.container {
		padding-bottom: 3em;
	}

	.work-element {
		width: 70%;
		max-width: 400px;
		margin-left: auto;

		.name {
			font-size: 1.2em;
			font-weight: 700;
			margin-top: 0.4em;
		}

		.description {
			font-size: 0.9em;
			margin-top: 0.4em;
			height: 10ch;
		}

		.image a {
			opacity: 1;
			background: none;
		}

		& :global(img) {
			width: 100%;
			height: auto;
			border: solid 1px rgba(240, 240, 240, 0.6);
		}

		& + .work-element {
			margin-top: 7em;
		}
	}

	.right {
		margin-top: 8em;

		.work-element {
			margin-left: 0;
			margin-right: auto;

			& :global(img) {
				border: solid 1px rgba(32, 32, 32, 0.6);
			}
		}
	}

	@media screen and (max-width: 700px) {
		.work-element {
			width: 100%;
			margin-left: auto !important;
			margin-right: auto !important;
			text-align: left;

			.description {
				height: auto;
			}

			& + .work-element {
				margin-top: 1.6em;
			}
		}

		.right {
			h2 {
				display: none;
			}

			margin-top: 1.6em;
		}
	}
</style>

<div class="container">
	<div class="left">
		<h2>My works</h2>

		<div class="work-element">
			<div class="image">
				<a href="https://yaav.leonardini.dev" target="_blank" rel="noreferrer"
					><Lazyload
						src="/assets/yaav.jpg"
						alt="YAAV - Yet Another Algorithm Visualizer"
						height="283"
						width="100%" /></a>
			</div>
			<div class="name">YAAV - Yet Another Algorithm Visualizer</div>
			<div class="description">
				(In progress) My own take at an algorithm visualizer, built with collaboration and expansion
				in mind. Aiming not only at sorting and graph algorithms, but also computer vision, search,
				games and many others.
			</div>
		</div>

		<div class="work-element">
			<div class="image">
				<Lazyload
					src="/assets/overdrive.jpg"
					alt="PCB layout of an overdrive pedal"
					height="283"
					width="100%" />
			</div>
			<div class="name">Analog Electronics</div>
			<div class="description">
				While it's not open source (not yet anyway), I like to study and fiddle with analog
				circuits, especially related to audio signal chains and effetcs, such as guitar pedals. I
				"design", plan, solder and build everything, from the PCB to the enclosure. I'm not always
				sure what I'm doing, though.
			</div>
		</div>

		<div class="work-element">
			<div class="image">
				<Lazyload
					src="/assets/felpe.jpg"
					alt="Screenshot of a web platform for ordering sweaters"
					height="283"
					width="100%" />
			</div>
			<div class="name">Web platforms</div>
			<div class="description">
				I develop web platform for various scopes, such as school events (with associated bookings)
				and school merchandise (t-shirts and sweaters orders).
			</div>
		</div>
	</div>
	<div class="right">
		<h2>&nbsp;</h2>

		<div class="work-element">
			<div class="image">
				<a href="https://papillegustative.com" target="_blank" rel="noreferrer"
					><Lazyload
						src="/assets/papille.jpg"
						alt="Screenshot of my band's website"
						height="283"
						width="100%" /></a>
			</div>
			<div class="name">:Papille Gustative</div>
			<div class="description">
				My musical interests and hackiness come together when I manage every technical aspect of my
				band. Other than the website, I'm planning MIDI and DMX softwares to controls our live
				shows.
			</div>
		</div>

		<div class="work-element">
			<div class="image">
				<a href="https://music.leonardini.dev" target="_blank" rel="noreferrer"
					><Lazyload
						src="/assets/music.jpg"
						alt="Screenshot of my music page"
						height="283"
						width="100%" /></a>
			</div>
			<div class="name">Music</div>
			<div class="description">
				After years of playing musical instruments, recently I've decided to start composing,
				arranging and producing my personal stuff. I also do non-critical mixing and mastering for
				my band.
			</div>
		</div>
	</div>
</div>
