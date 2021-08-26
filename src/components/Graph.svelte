<script lang="ts">
	import { onMount } from 'svelte';
	
	type Node = {
		x :number,
		y :number,
		direction :number
	}

	const lightColor = '240,240,240';
	const darkColor = '32,32,32';

	let container :HTMLElement;
	let placeholder :HTMLElement;
	let width :number, height :number;
	let canvas :HTMLCanvasElement;
	let ctx :CanvasRenderingContext2D;

	const nodes_count = 70;
	const mobile_limit = .5;

	const nodes :Array<Node> = new Array(nodes_count);

	const createNode = () :Node => {
		return {
			x: Math.floor(Math.random() * (width / 100 + 1)) * 100,
            y: Math.floor(Math.random() * (height / 100 + 1)) * 100,
            direction: Math.random() * (Math.PI * 2 + 1)
		}
	}

	const color = (node :Node) :string => {
		if (width < height)
			return lightColor;
		return node.x > (width / 2)
			? darkColor
			: lightColor;
	}
	
	const resizeHandler = () => {
		const toMoveAround = nodes[0] == undefined 
			|| canvas.width !== canvas.clientWidth * window.devicePixelRatio;

		if(window.innerWidth <= 700) {
			container.style.height = `${document.querySelector('.container.ontop').clientHeight}px`;
		}

		canvas.width = Math.floor(canvas.clientWidth * window.devicePixelRatio);
		canvas.height = Math.floor(canvas.clientHeight * window.devicePixelRatio);
		width = canvas.width;
		height = canvas.height;

		if(toMoveAround) {
			for (let i = 0; i < nodes_count; i++) {
				nodes[i] = createNode();
			}
		}
	}
	
	onMount(() => {
		let shouldRender = true;
		
		container.removeChild(placeholder);
		canvas.style.display = 'block';

		ctx = canvas.getContext('2d');

		document.body.onresize = resizeHandler;
		resizeHandler();
		
		const intersectionObserver = new IntersectionObserver((entries) => {
			entries.forEach(entry => {
				shouldRender = entry.isIntersecting;
			});
		});
		intersectionObserver.observe(canvas);

		const speed = 0.1;
		function animate() {
			const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

			// Check if the media query matches or is not available.
			if (mediaQuery && !mediaQuery.matches) {
				requestAnimationFrame(animate);
			}

			if(!shouldRender) return;

			// Clear
			ctx.clearRect(0, 0, width, height);

			for(let i in nodes) {
				if(width < height && (i as any) > nodes_count * mobile_limit) {
					break;
				}
				nodes[i].x += Math.cos(nodes[i].direction) * speed;
				nodes[i].y += Math.sin(nodes[i].direction) * speed;

				while(nodes[i].x < 0)
					nodes[i].x += width;
				nodes[i].x %= width;

				while(nodes[i].y < 0)
					nodes[i].y += height;
				nodes[i].y %= height;

				// Render node
				ctx.fillStyle = `rgba(${color(nodes[i])},0.6)`;
				ctx.beginPath();
				ctx.arc(nodes[i].x, nodes[i].y, 2, 0, Math.PI * 2, true);
				ctx.fill();

				for(let j in nodes) {
					if(width < height && (j as any) > nodes_count * mobile_limit) {
						break;
					}
					if (j <= i) {
						continue;
					}

					let dx = Math.abs(nodes[i].x - nodes[j].x);
					let dy = Math.abs(nodes[i].y - nodes[j].y);
					let d = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));

					let alpha = 0;
					if (d <= 300) {
						alpha = 0.8 - ((0.8 * d) / 200);
					}

					if (alpha == 0) {
						continue;
					}

					ctx.lineWidth = 1;
					if((nodes[i].x - width / 2) * (nodes[j].x - width / 2) < 0) {
						const intermediary = (nodes[j].y - nodes[i].y) * (width / 2 - nodes[i].x) / (nodes[j].x - nodes[i].x) + nodes[i].y;

						ctx.strokeStyle = `rgba(${color(nodes[i])},${alpha})`;
						ctx.beginPath();
						ctx.moveTo(nodes[i].x, nodes[i].y);
						ctx.lineTo(width / 2, intermediary);
						ctx.stroke();

						ctx.strokeStyle = `rgba(${color(nodes[j])},${alpha})`;
						ctx.beginPath();
						ctx.moveTo(width / 2, intermediary);
						ctx.lineTo(nodes[j].x, nodes[j].y);
						ctx.stroke();
					} else {
						ctx.strokeStyle = `rgba(${color(nodes[i])},${alpha})`;
						ctx.beginPath();
						ctx.moveTo(nodes[i].x, nodes[i].y);
						ctx.lineTo(nodes[j].x, nodes[j].y);
						ctx.stroke();
					}
				}
			}
		}
		animate();
	})
</script>

<style>
	div.graph-container {
		height: 100vh;
		max-height: 1080px;
	}

	div.placeholder, canvas#graph {
		width: 100%;
		height: 100%;
	}
</style>

<div bind:this={container} class="graph-container">
	<div class="placeholder" bind:this={placeholder}></div>
	<!-- Based on and modified from https://github.com/rohanrhu/nodes.js -->
	<canvas id="graph" style="display: none;" bind:this={canvas}></canvas>
</div>
