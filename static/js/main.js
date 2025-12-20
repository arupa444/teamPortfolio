// Register GSAP Plugin
gsap.registerPlugin(ScrollTrigger);

// 1. THREE.JS PARTICLE BACKGROUND
const initThreeJS = () => {
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    // Particles
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 700;
    const posArray = new Float32Array(particlesCount * 3);

    for(let i = 0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 25; // Spread
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const material = new THREE.PointsMaterial({
        size: 0.02,
        color: 0x06b6d4, // Cyan
        transparent: true,
        opacity: 0.8
    });

    const particlesMesh = new THREE.Points(particlesGeometry, material);
    scene.add(particlesMesh);
    camera.position.z = 5;

    // Animation Loop
    let mouseX = 0;
    let mouseY = 0;

    const animate = () => {
        requestAnimationFrame(animate);
        particlesMesh.rotation.y += 0.001;
        particlesMesh.rotation.x += 0.0005;

        // Mouse interaction
        particlesMesh.rotation.y += mouseX * 0.0005;
        particlesMesh.rotation.x += mouseY * 0.0005;

        renderer.render(scene, camera);
    };
    animate();

    // Resize Handle
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Mouse Move
    document.addEventListener('mousemove', (event) => {
        mouseX = event.clientX - window.innerWidth / 2;
        mouseY = event.clientY - window.innerHeight / 2;
    });
};

// 2. GSAP ANIMATIONS
const initAnimations = () => {
    // Hero Text Reveal
    gsap.from(".hero-text", {
        duration: 1.5,
        y: 100,
        opacity: 0,
        ease: "power4.out",
        delay: 0.2
    });
    gsap.from(".hero-sub", {
        duration: 1.5,
        y: 50,
        opacity: 0,
        ease: "power4.out",
        delay: 0.4
    });
    gsap.from(".hero-cta", {
        duration: 1.5,
        y: 50,
        opacity: 0,
        ease: "power4.out",
        delay: 0.6
    });

    // Section Headers
    gsap.utils.toArray('section h2').forEach(header => {
        gsap.from(header, {
            scrollTrigger: {
                trigger: header,
                start: "top 80%",
            },
            y: 50,
            opacity: 0,
            duration: 1
        });
    });

    // Team Cards Stagger
    gsap.from(".team-card", {
        scrollTrigger: {
            trigger: "#team",
            start: "top 70%",
        },
        y: 100,
        opacity: 0,
        duration: 0.8,
        stagger: 0.2,
        ease: "back.out(1.7)"
    });

    // Project Rows Slide In
    gsap.utils.toArray('.project-row').forEach(row => {
        gsap.from(row, {
            scrollTrigger: {
                trigger: row,
                start: "top 85%",
            },
            x: -50,
            opacity: 0,
            duration: 1,
            ease: "power2.out"
        });
    });
};



// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initThreeJS();
    initAnimations();
});