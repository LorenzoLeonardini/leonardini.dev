<script lang="ts">
	import { onMount } from 'svelte';
	import { Scene, PerspectiveCamera, WebGLRenderer, LineBasicMaterial, BufferGeometry, Line,
		PlaneGeometry, CircleGeometry, Mesh, MeshBasicMaterial, Vector3, Color, BufferAttribute } from 'three';

	let container :HTMLElement;
	
	onMount(() => {
		const lightColor = new Color(0xf0f0f0);
		const darkColor = new Color(0x202020);
		let shouldRender = true;
		
		const canvas :HTMLCanvasElement = document.querySelector('canvas#graph');
		const intersectionObserver = new IntersectionObserver((entries) => {
			entries.forEach(entry => {
				shouldRender = entry.isIntersecting;
			});
		});
		intersectionObserver.observe(canvas);

		const scene = new Scene();
		const camera = new PerspectiveCamera(75, 2, 0.1, 1000);
		const renderer = new WebGLRenderer({ canvas, antialias: true });
		canvas.style.display = 'block';
		container.removeChild(document.querySelector('.placeholder'));

		const backgroundGeometry = new PlaneGeometry(window.innerWidth / 2, window.innerHeight);
		const leftBackgroundMaterial = new MeshBasicMaterial({ color: 0x202020 });
		const leftBackground = new Mesh(backgroundGeometry, leftBackgroundMaterial);
		leftBackground.position.z = -100;
		leftBackground.position.x = -window.innerWidth / 4;
		scene.add(leftBackground);

		const rightBackgroundMaterial = new MeshBasicMaterial({ color: 0xf0f0f0 });
		const rightBackground = new Mesh(backgroundGeometry, rightBackgroundMaterial);
		rightBackground.position.z = -100;
		rightBackground.position.x = window.innerWidth / 4;
		scene.add(rightBackground);

		const pointGeometry = new CircleGeometry(.03, 32);

		function viewportWidth() {
			return ((window.innerWidth / window.innerHeight) * 9);
		}

		function viewportHeight() {
			return 9;
		}

		function updateGeometryPosition(geometry, index, position) {
			geometry.attributes.position.array[3 * index + 0] = position.x;
			geometry.attributes.position.array[3 * index + 1] = position.y;
			geometry.attributes.position.array[3 * index + 2] = position.z;
		}

		function resizeRendererToDisplaySize(renderer) {
			const canvas = renderer.domElement;
			const width = canvas.clientWidth;
			const height = canvas.clientHeight;
			const needResize = canvas.width !== width || canvas.height !== height;
			if (needResize) {
				renderer.setSize(width, height, false);
			}
			return needResize;
		}

		const points = [];
		for(let i = 0; i < 40; i++) {
			const material = new MeshBasicMaterial({ color: 0xf0f0f0 });
			material.transparent = true;
			material.opacity = .6;
			const point = new Mesh(pointGeometry, material);
			point.position.x = Math.floor(Math.random() * viewportWidth()) - viewportWidth() / 2;
			point.position.y = Math.floor(Math.random() * viewportHeight()) - viewportHeight() / 2;
			points.push([
				point,
				Math.random() * (Math.PI * 2 + 1),
				material
			])
			scene.add(point);
		}

		const lines = [];
		for(let i = 0; i < points.length * 3; i++) {
			const material = new LineBasicMaterial({ color: 0xffffff });
			material.transparent = true;
			const geometry = new BufferGeometry();
			const positions = new Float32Array(2 * 3); // 3 vertices per point
			geometry.setAttribute('position', new BufferAttribute(positions, 3));
			const drawCount = 2; // draw the first 2 points
			geometry.setDrawRange(0, drawCount);
			const line = new Line(geometry, material);
			scene.add(line);
			lines.push({
				material,
				geometry,
				line
			});
		}

		camera.position.z = 5;

		const speed = 0.002;
		function animate() {
			const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

			// Check if the media query matches or is not available.
			if (mediaQuery && !mediaQuery.matches) {
				requestAnimationFrame(animate);
			}

			if(!shouldRender) return;

			let lineIdx = 0;
			for(let i in points) {
				const point = points[i][0];
				point.translateX(Math.cos(points[i][1]) * speed);
				point.translateY(Math.sin(points[i][1]) * speed);

				if(point.position.x > 0) {
					points[i][2].color = darkColor;
				} else {
					points[i][2].color = lightColor;
				}

				while(point.position.x > viewportWidth() / 2) {
					point.translateX(-viewportWidth());
				}
				while(point.position.x < -viewportWidth() / 2) {
					point.translateX(viewportWidth());
				}

				while(point.position.y > viewportHeight() / 2) {
					point.translateY(-viewportHeight());
				}
				while(point.position.y < -viewportHeight() / 2) {
					point.translateY(viewportHeight());
				}

				for(let j in points) {
					if(j <= i || lineIdx >= lines.length) {
						continue;
					}

					const d = points[i][0].position.distanceTo(points[j][0].position);
					if(d > 3) {
						continue;
					}
					const line = lines[lineIdx++];
					line.material.opacity = 1 - ((0.6 * d) / 2);
					line.material.color = points[i][0].position.x < 0 ? lightColor : darkColor

					updateGeometryPosition(line.geometry, 0, points[i][0].position);
					updateGeometryPosition(line.geometry, 1, points[j][0].position);
					line.geometry.attributes.position.needsUpdate = true;
					line.geometry.computeBoundingBox();
					line.geometry.computeBoundingSphere();

					if((points[i][0].position.x < 0 && points[j][0].position.x >= 0)
						|| (points[j][0].position.x < 0 && points[i][0].position.x >= 0)) {
						const x1 = points[i][0].position.x;
						const y1 = points[i][0].position.y;
						const x2 = points[j][0].position.x;
						const y2 = points[j][0].position.y;
						const intermediary = (y2 - y1) * (-x1) / (x2 - x1) + y1;

						updateGeometryPosition(line.geometry, 0, points[i][0].position);
						updateGeometryPosition(line.geometry, 1, {x: 0, y: intermediary, z: 0});
						line.material.color = points[i][0].position.x < 0 ? lightColor : darkColor;

						if(lineIdx < lines.length) {
							const line2 = lines[lineIdx++];
							updateGeometryPosition(line2.geometry, 0, points[j][0].position);
							updateGeometryPosition(line2.geometry, 1, {x: 0, y: intermediary, z: 0});
							line2.geometry.attributes.position.needsUpdate = true;
							line2.geometry.computeBoundingBox();
							line2.geometry.computeBoundingSphere();

							line2.material.opacity = line.material.opacity;
							line2.material.color = points[j][0].position.x < 0 ? lightColor : darkColor;
						}
					}
				}
			}
			while(lineIdx < lines.length) {
				lines[lineIdx++].material.opacity = 0;
			}

			if(resizeRendererToDisplaySize(renderer)) {
				camera.aspect = canvas.clientWidth / canvas.clientHeight;
				camera.updateProjectionMatrix();
			}

			renderer.render(scene, camera);
		}
		animate();
	})
</script>

<style>
	div.placeholder, canvas#graph {
		width: 100%;
		height: 100vh;
	}

	div.placeholder {
		background: #202020;
		background: linear-gradient(90deg, #202020 0%, #202020 50%, #f0f0f0 50%, #f0f0f0 100%);
	}
</style>

<div bind:this={container}>
	<div class="placeholder"></div>
	<canvas id="graph" style="display: none;"></canvas>
</div>