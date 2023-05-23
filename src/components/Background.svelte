<style lang="scss">
	.background-elements-container {
		grid-area: left / left / left / right;
		padding: 2em 0 2.5em 0;

		.background-element {
			padding: 1em 0;
			width: 50%;
			padding-left: 5em;
			transform: translateX(100%);
			color: var(--light);

			.date {
				position: relative;
				left: -3.5rem;
				font-size: 0.8em;
				--line-size: 3px;
				--size: 50px;

				&::before {
					content: '';
					position: absolute;
					left: calc(-1.5rem - (var(--size) / 2));
					width: var(--size);
					height: var(--size);
					border-radius: 50%;
					background: var(--light);
					border: solid var(--line-size) var(--dark);
				}

				&::after {
					content: '';
					position: absolute;
					width: 8rem;
					height: var(--line-size);
					background: var(--light);
					left: -1rem;
					top: calc(var(--size) / 2);
					transform: translateY(calc(var(--line-size) * (-0.5)));
				}
			}

			.title {
				font-weight: 700;
				font-size: 1.2em;
				position: relative;
				top: -0.1em;
				left: 3.5em;
				display: inline-block;
				max-width: calc(100% - 3.5em);
			}

			.description {
				font-size: 0.9em;
				margin-top: 0.4em;
			}
		}
	}

	@media screen and (orientation: landscape) {
		.background-elements-container {
			.background-element {
				&:nth-child(even) {
					transform: translateX(0);
					padding-left: 0;
					padding-right: 5rem;
					text-align: right;
					color: var(--dark);

					a {
						color: var(--darker-blue);
						opacity: 1;
						background-image: linear-gradient(var(--darker-blue), var(--darker-blue));
						background-position: right bottom;
						background-size: 100% 3px;
					}

					a:hover {
						background-size: 0% 3px;
					}

					.date {
						left: auto;
						right: -3.5rem;

						&::before {
							--line-size: 2px;
							left: auto;
							right: calc(-1.5rem - (var(--size) / 2));
							background: var(--dark);
							border: solid var(--line-size) var(--light);
						}

						&::after {
							background: var(--dark);
							left: auto;
							right: -1rem;
						}
					}

					.title {
						left: auto;
						right: 3.5em;
					}
				}
			}
		}
	}

	@media screen and (orientation: portrait) {
		.background-elements-container {
			overflow-x: hidden;

			.background-element {
				width: 100%;
				transform: translateX(0%);

				.date {
					left: -3.5rem;
					top: 0.6rem;
					--line-size: 2px;
					--size: 30px;

					&::before {
						background: none;
						border: solid var(--line-size) var(--light);
						left: calc(-1.5rem - (var(--size) / 2));
					}
					&::after {
						width: 6.5rem;
						left: -0.5rem;
						top: calc((var(--size) / 2));
					}
				}

				.title {
					left: 2.5em;
				}

				.description {
					position: relative;
					left: -2em;
				}
			}
		}
	}
</style>

<div class="background-elements-container">
	<div class="background-element">
		<div class="date">2022-present</div>
		<div class="title">CyberSecurity Consultant & Developer</div>
		<div class="description">
			I'm currently working as a freelance cybersecurity consultant and developer, performing VAPT
			and WAPT activities, developing web applications, mainly using Svelte, and <a
				href="https://hub.docker.com/r/cybersecnatlab/challenge-headless"
				target="_blank"
				rel="noreferrer noopener">tools</a> for Capture the Flag (CTF) competitions.
		</div>
	</div>

	<div class="background-element">
		<div class="date">2019-present</div>
		<div class="title">University of Pisa</div>
		<div class="description">
			After getting my Bachelor's degree, with a thesis titled <em
				>Practical comparison of E2EE algorithms of instant messaging app</em
			>, I'm currently studying to get my Master's degree in Computer Science.
		</div>
	</div>

	<div class="background-element">
		<div class="date">2021</div>
		<div class="title">CyberChallenge.IT</div>
		<div class="description">
			Second partecipation to the Italian program for cyber security. I placed first at the local
			competition, and helped my team get third at the national one. I was selected to be one of the
			ten people in the <a href="https://teamitaly.eu/" target="_blank" rel="noreferrer"
				>Italian team</a> for the European Cyber Security Challenge held in Prague.
		</div>
	</div>

	<div class="background-element">
		<div class="date">2018</div>
		<div class="title">CyberChallenge.IT</div>
		<div class="description">
			Italian initiative to introduce young students to the field of cyber security. I've had the
			chance to <a href="https://teamitaly.eu/2018.html" target="_blank" rel="noreferrer"
				>join the Italian team</a> in London for the European Cyber Security Challenge.
		</div>
	</div>

	<div class="background-element">
		<div class="date">2017-2019</div>
		<div class="title">Programming and security competitions</div>
		<div class="description">
			I play Capture The Flag (CTF) competitions with University of Genoa's team, <a
				href="https://zenhack.it"
				target="_blank"
				rel="noreferrer">ZenHack</a
			>.<br /><br />I partecipated in different competitive programming competitions, such as the
			Italian Olympiad in Informatics (OII) and the Reply Code Challenge.
		</div>
	</div>

	<div class="background-element">
		<div class="date">always</div>
		<div class="title">Self-teaching</div>
		<div class="description">
			Before enrollin in university, excluding some rare opportunities, I've always studied
			programming and computer science as a self-taught person. This led to good problem solving
			skills when facing different issues. I still keep learning by myself most of the stuff I'm
			passionate about.
		</div>
	</div>

	<div class="background-element">
		<div class="date">2013-2019</div>
		<div class="title">Liceo Scientifico G.D. Cassini</div>
		<div class="description">
			I've attended a standard scientific high school in Genoa, while at the same time I was
			spending my free time fiddling around writing code.
		</div>
	</div>
</div>
