// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector('#bg'),
    alpha: true
});

renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
camera.position.setZ(30);

// Create particles
const particlesGeometry = new THREE.BufferGeometry();
const particlesCount = 2000;
const posArray = new Float32Array(particlesCount * 3);

for(let i = 0; i < particlesCount * 3; i += 3) {
    posArray[i] = (Math.random() - 0.5) * 100;
    posArray[i+1] = (Math.random() - 0.5) * 100;
    posArray[i+2] = (Math.random() - 0.5) * 100;
}

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

const particlesMaterial = new THREE.PointsMaterial({
    size: 0.2,
    color: 0x00ffcc,
    transparent: true,
    opacity: 0.6,
    blending: THREE.AdditiveBlending
});

const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particlesMesh);

// Create central geometric shapes
const ringGeometry = new THREE.TorusGeometry(8, 0.5, 16, 100);
const ringMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x00ffcc,
    emissive: 0x004433,
    transparent: true,
    opacity: 0.3
});
const ring = new THREE.Mesh(ringGeometry, ringMaterial);
scene.add(ring);

const ring2Geometry = new THREE.TorusGeometry(12, 0.3, 16, 100);
const ring2Material = new THREE.MeshStandardMaterial({ 
    color: 0x00ccff,
    emissive: 0x003344,
    transparent: true,
    opacity: 0.2
});
const ring2 = new THREE.Mesh(ring2Geometry, ring2Material);
ring2.rotation.x = Math.PI / 2;
scene.add(ring2);

// Create floating orbs
const sphereGeometry = new THREE.SphereGeometry(0.5, 32, 32);
const sphereMaterial = new THREE.MeshStandardMaterial({ 
    color: 0x00ffcc,
    emissive: 0x004433
});

const orbs = [];
for(let i = 0; i < 20; i++) {
    const orb = new THREE.Mesh(sphereGeometry, sphereMaterial);
    orb.position.x = (Math.random() - 0.5) * 50;
    orb.position.y = (Math.random() - 0.5) * 50;
    orb.position.z = (Math.random() - 0.5) * 50;
    orb.userData = {
        speed: 0.002 + Math.random() * 0.003,
        angle: Math.random() * Math.PI * 2
    };
    scene.add(orb);
    orbs.push(orb);
}

// Lighting
const ambientLight = new THREE.AmbientLight(0x404060);
scene.add(ambientLight);

const pointLight1 = new THREE.PointLight(0x00ffcc, 1, 50);
pointLight1.position.set(10, 10, 10);
scene.add(pointLight1);

const pointLight2 = new THREE.PointLight(0x00ccff, 1, 50);
pointLight2.position.set(-10, -10, 10);
scene.add(pointLight2);

const pointLight3 = new THREE.PointLight(0xff00ff, 0.5, 50);
pointLight3.position.set(0, 0, 20);
scene.add(pointLight3);

// Animation
function animate() {
    requestAnimationFrame(animate);
    
    // Rotate rings
    ring.rotation.x += 0.001;
    ring.rotation.y += 0.002;
    ring2.rotation.y += 0.001;
    
    // Rotate particles
    particlesMesh.rotation.y += 0.0002;
    particlesMesh.rotation.x += 0.0001;
    
    // Animate orbs
    orbs.forEach(orb => {
        orb.rotation.x += 0.01;
        orb.rotation.y += 0.01;
        orb.position.y += Math.sin(Date.now() * orb.userData.speed) * 0.01;
    });
    
    renderer.render(scene, camera);
}

animate();

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});