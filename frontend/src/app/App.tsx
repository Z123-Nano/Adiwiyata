import GardenCanvas from '../scene/GardenCanvas'
import InspectionPanel from '../scene/InspectionPanel'

export default function App() {
  return (
    <div style={{ height: '100vh', width: '100vw', background: '#0b0c15' }}>
      <h1 style={{ position: 'absolute', top: 12, left: 12, color: '#fff', zIndex: 10, fontFamily: 'system-ui, sans-serif', margin: 0, fontSize: 16 }}>
        My Digital Twin Garden — synthetic viewer (TASK 004)
      </h1>
      <GardenCanvas />
      <InspectionPanel />
    </div>
  )
}
