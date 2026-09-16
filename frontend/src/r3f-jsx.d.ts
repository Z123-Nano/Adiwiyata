import { JSX } from 'react'

declare module 'react' {
  namespace JSX {
    interface IntrinsicElements {
      ambientLight: any
      directionalLight: any
      mesh: any
      boxGeometry: any
      meshStandardMaterial: any
      orbitControls: any
      group: any
      coneGeometry: any
      cylinderGeometry: any
      sphereGeometry: any
      gridHelper: any
      planeGeometry: any
      line: any
    }
  }
}
