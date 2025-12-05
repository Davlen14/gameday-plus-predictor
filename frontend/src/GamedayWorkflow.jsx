import React, { useState, useRef, useEffect, useCallback } from 'react';
import { 
  Play, Save, Settings, Plus, Search, X, 
  ChevronRight, ChevronDown, Zap, Database, 
  Cpu, UploadCloud, Activity, AlertCircle, 
  CheckCircle2, Terminal, ZoomIn, ZoomOut, 
  MousePointer2, Trash2, MoreVertical
} from 'lucide-react';

// --- Constants & Styles ---

const NODE_WIDTH = 240;
const NODE_HEIGHT = 120; // Base height, can expand
const PORT_RADIUS = 6;

const COLORS = {
  trigger: { bg: 'bg-emerald-500', text: 'text-emerald-500', border: 'border-emerald-500', glow: 'shadow-emerald-500/20' },
  source: { bg: 'bg-blue-500', text: 'text-blue-500', border: 'border-blue-500', glow: 'shadow-blue-500/20' },
  process: { bg: 'bg-purple-500', text: 'text-purple-500', border: 'border-purple-500', glow: 'shadow-purple-500/20' },
  output: { bg: 'bg-amber-500', text: 'text-amber-500', border: 'border-amber-500', glow: 'shadow-amber-500/20' },
};

const INITIAL_NODES = [
  { id: '1', type: 'trigger', title: 'Game Start Webhook', x: 100, y: 150, status: 'idle', data: { method: 'POST', endpoint: '/api/v1/gamestart' } },
  { id: '2', type: 'source', title: 'Player Stats DB', x: 450, y: 50, status: 'idle', data: { query: 'SELECT * FROM players WHERE active=1' } },
  { id: '3', type: 'source', title: 'Live Odds API', x: 450, y: 250, status: 'idle', data: { provider: 'SportRadar', refresh: '5s' } },
  { id: '4', type: 'process', title: 'Data Merger', x: 800, y: 150, status: 'idle', data: { strategy: 'inner_join', key: 'player_id' } },
  { id: '5', type: 'process', title: 'Predictive Model', x: 1150, y: 150, status: 'idle', data: { model: 'v2.4-production', threshold: 0.85 } },
  { id: '6', type: 'output', title: 'Frontend Push', x: 1500, y: 150, status: 'idle', data: { channel: 'websocket-secure', topic: 'live-updates' } },
];

const INITIAL_CONNECTIONS = [
  { id: 'c1', source: '1', target: '2' },
  { id: 'c1b', source: '1', target: '3' },
  { id: 'c2', source: '2', target: '4' },
  { id: 'c3', source: '3', target: '4' },
  { id: 'c4', source: '4', target: '5' },
  { id: 'c5', source: '5', target: '6' },
];

const LOGS = [
  { time: '10:42:01', level: 'info', msg: 'System initialized. Ready for gameday events.' },
  { time: '10:42:05', level: 'success', msg: 'Connected to Player Stats Database (latency: 12ms).' },
  { time: '10:42:05', level: 'success', msg: 'Odds API socket established.' },
];

// --- Components ---

const TopNav = ({ onRun, isRunning }) => (
  <div className="h-14 bg-[#1a1a1a] border-b border-gray-800 flex items-center justify-between px-4 z-20 relative">
    <div className="flex items-center gap-3">
      <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-500/20">
        <Activity className="text-white w-5 h-5" />
      </div>
      <div>
        <h1 className="text-white font-bold text-sm tracking-wide">GAMEDAY<span className="text-indigo-400">+</span></h1>
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="text-[10px] text-gray-400 uppercase tracking-wider font-medium">System Online</span>
        </div>
      </div>
    </div>

    <div className="flex items-center gap-2">
      <button className="px-3 py-1.5 text-xs font-medium text-gray-300 hover:text-white hover:bg-white/10rounded-md transition-colors">
        Drafts / NFL-Sunday-Flow
      </button>
    </div>

    <div className="flex items-center gap-3">
      <button 
        onClick={onRun}
        disabled={isRunning}
        className={`flex items-center gap-2 px-4 py-1.5 rounded-md text-sm font-semibold transition-all ${
          isRunning 
            ? 'backdrop-blur-sm text-gray-500 cursor-not-allowed border border-white/5' 
            : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-900/50'
        }`}
      >
        {isRunning ? <div className="animate-spin w-4 h-4 border-2 border-gray-500 border-t-transparent rounded-full" /> : <Play className="w-4 h-4 fill-current" />}
        {isRunning ? 'Running...' : 'Test Flow'}
      </button>
      <button className="p-2 text-gray-400 hover:text-white hover:bg-white/10rounded-md transition-colors">
        <Save className="w-5 h-5" />
      </button>
      <div className="w-8 h-8 bg-gradient-to-r from-pink-500 to-rose-500 rounded-full border-2 border-[#1a1a1a] cursor-pointer" />
    </div>
  </div>
);

const SidebarItem = ({ icon: Icon, label, type, onAdd }) => {
  const color = COLORS[type];
  return (
    <div 
      className="group flex items-center gap-3 p-3 rounded-lg hover:bg-white/10cursor-grab active:cursor-grabbing border border-transparent hover:border-gray-700 transition-all mb-2"
      onClick={() => onAdd(type, label)}
    >
      <div className={`w-8 h-8 rounded-md ${color.bg} bg-opacity-20 flex items-center justify-center group-hover:bg-opacity-30 transition-all`}>
        <Icon className={`w-4 h-4 ${color.text}`} />
      </div>
      <span className="text-gray-300 text-sm font-medium">{label}</span>
      <div className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity">
        <Plus className="w-4 h-4 text-gray-500" />
      </div>
    </div>
  );
};

const Node = ({ node, isSelected, onClick, onMouseDown, zoom }) => {
  const color = COLORS[node.type];
  
  // Choose Icon
  let Icon = Activity;
  if (node.type === 'trigger') Icon = Zap;
  if (node.type === 'source') Icon = Database;
  if (node.type === 'process') Icon = Cpu;
  if (node.type === 'output') Icon = UploadCloud;

  return (
    <div
      style={{
        transform: `translate(${node.x}px, ${node.y}px)`,
        width: NODE_WIDTH,
        position: 'absolute',
      }}
      className={`group rounded-xl backdrop-blur-md transition-shadow duration-300
        ${isSelected ? `ring-2 ring-offset-2 ring-offset-[#1a1a1a] ${color.border} shadow-xl ${color.glow}` : 'border border-gray-800 hover:border-gray-600 shadow-lg shadow-black/40'}
        bg-[#242424]/90
      `}
      onMouseDown={(e) => onMouseDown(e, node.id)}
      onClick={(e) => {
        e.stopPropagation();
        onClick(node.id);
      }}
    >
      {/* Input Port (Left) */}
      {node.type !== 'trigger' && (
        <div className="absolute top-1/2 -left-3 -translate-y-1/2 w-6 h-6 flex items-center justify-center cursor-crosshair group/port">
           <div className={`w-3 h-3 rounded-full border-2 border-gray-600 bg-[#1a1a1a] group-hover/port:border-white transition-colors`} />
        </div>
      )}

      {/* Output Port (Right) */}
      {node.type !== 'output' && (
        <div 
          className="absolute top-1/2 -right-3 -translate-y-1/2 w-6 h-6 flex items-center justify-center cursor-crosshair group/port"
          data-node-id={node.id}
          data-port-type="output"
        >
          <div className={`w-3 h-3 rounded-full border-2 border-gray-600 bg-[#1a1a1a] group-hover/port:${color.border} group-hover/port:bg-${color.bg} transition-colors`} />
        </div>
      )}

      {/* Header */}
      <div className="flex items-center gap-3 p-3 border-b border-gray-800/50">
        <div className={`w-8 h-8 rounded-lg ${color.bg} flex items-center justify-center text-white shadow-inner`}>
          <Icon className="w-4 h-4" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="text-gray-200 text-sm font-semibold truncate">{node.title}</div>
          <div className="text-[10px] text-gray-500 font-mono uppercase tracking-wider">{node.type}</div>
        </div>
        {node.status === 'running' && <div className="w-2 h-2 rounded-full bg-amber-400 animate-ping" />}
        {node.status === 'success' && <CheckCircle2 className="w-4 h-4 text-emerald-500" />}
        {node.status === 'error' && <AlertCircle className="w-4 h-4 text-red-500" />}
      </div>

      {/* Body */}
      <div className="p-3">
        <div className="space-y-2">
          {Object.entries(node.data).slice(0, 2).map(([key, value]) => (
            <div key={key} className="flex items-center justify-between text-xs">
              <span className="text-gray-500 capitalize">{key}:</span>
              <span className="text-gray-300 font-mono bg-black/30 px-1.5 py-0.5 rounded max-w-[120px] truncate">
                {value}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const Connection = ({ start, end, active }) => {
  const controlPointOffset = Math.abs(end.x - start.x) * 0.5;
  const path = `M ${start.x} ${start.y} C ${start.x + controlPointOffset} ${start.y}, ${end.x - controlPointOffset} ${end.y}, ${end.x} ${end.y}`;

  return (
    <g>
      {/* Shadow/Base Line */}
      <path
        d={path}
        fill="none"
        stroke="#1a1a1a"
        strokeWidth="6"
      />
      {/* Visible Line */}
      <path
        d={path}
        fill="none"
        stroke={active ? '#6366f1' : '#4b5563'}
        strokeWidth="2"
        className="transition-colors duration-300"
      />
      {/* Active Animation */}
      {active && (
        <circle r="4" fill="#818cf8">
          <animateMotion dur="1s" repeatCount="indefinite" path={path} />
        </circle>
      )}
      {active && (
        <circle r="2" fill="white" opacity="0.8">
          <animateMotion dur="1s" begin="0.1s" repeatCount="indefinite" path={path} />
        </circle>
      )}
    </g>
  );
};

// --- Main Application ---

export default function GamedayWorkflow() {
  const [nodes, setNodes] = useState(INITIAL_NODES);
  const [connections, setConnections] = useState(INITIAL_CONNECTIONS);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [logs, setLogs] = useState(LOGS);
  
  // Viewport State
  const [scale, setScale] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const [lastMousePos, setLastMousePos] = useState({ x: 0, y: 0 });

  // Dragging State
  const [draggingNodeId, setDraggingNodeId] = useState(null);
  
  // Connection State
  const [tempConnection, setTempConnection] = useState(null); // { startX, startY, endX, endY }

  // Simulation State
  const [isRunning, setIsRunning] = useState(false);

  const canvasRef = useRef(null);

  // --- Helpers ---
  
  const screenToWorld = useCallback((sx, sy) => {
    // Basic implementation assuming full screen minus offsets
    // In a real app we'd use getBoundingClientRect of canvas
    const rect = canvasRef.current?.getBoundingClientRect() || { left: 280, top: 56 };
    return {
      x: (sx - rect.left - pan.x) / scale,
      y: (sy - rect.top - pan.y) / scale
    };
  }, [pan, scale]);

  const getNodeCenter = (id) => {
    const n = nodes.find(x => x.id === id);
    if (!n) return { x: 0, y: 0 };
    return {
      in: { x: n.x, y: n.y + NODE_HEIGHT / 2 }, // Approximation
      out: { x: n.x + NODE_WIDTH, y: n.y + NODE_HEIGHT / 2 }
    };
  };

  // --- Handlers ---

  const handleMouseDown = (e) => {
    // Check if clicking output port
    if (e.target.dataset.portType === 'output') {
      const nodeId = e.target.dataset.nodeId;
      const node = nodes.find(n => n.id === nodeId);
      const startX = node.x + NODE_WIDTH;
      const startY = node.y + NODE_HEIGHT / 2; // Approximate center height
      
      const worldPos = screenToWorld(e.clientX, e.clientY);

      setTempConnection({
        sourceId: nodeId,
        startX,
        startY,
        endX: worldPos.x,
        endY: worldPos.y
      });
      return;
    }

    // Default to panning if background
    if (e.button === 0) { // Left click
      setIsPanning(true);
      setLastMousePos({ x: e.clientX, y: e.clientY });
    }
  };

  const handleNodeMouseDown = (e, id) => {
    e.stopPropagation();
    setDraggingNodeId(id);
    setSelectedNodeId(id);
    setLastMousePos({ x: e.clientX, y: e.clientY });
  };

  const handleMouseMove = (e) => {
    const deltaX = (e.clientX - lastMousePos.x);
    const deltaY = (e.clientY - lastMousePos.y);

    if (draggingNodeId) {
      setNodes(prev => prev.map(n => {
        if (n.id === draggingNodeId) {
          return { ...n, x: n.x + deltaX / scale, y: n.y + deltaY / scale };
        }
        return n;
      }));
      setLastMousePos({ x: e.clientX, y: e.clientY });
    } else if (isPanning) {
      setPan(prev => ({ x: prev.x + deltaX, y: prev.y + deltaY }));
      setLastMousePos({ x: e.clientX, y: e.clientY });
    } else if (tempConnection) {
      const worldPos = screenToWorld(e.clientX, e.clientY);
      setTempConnection(prev => ({ ...prev, endX: worldPos.x, endY: worldPos.y }));
    }
  };

  const handleMouseUp = (e) => {
    setDraggingNodeId(null);
    setIsPanning(false);

    if (tempConnection) {
      // Hit detection for input ports would go here
      // For this demo, let's just clear it unless we dropped on a node (simplification)
      // Real implementation requires detecting element under mouse
      
      // We will perform a simple distance check against all nodes for simplicity
      const worldPos = screenToWorld(e.clientX, e.clientY);
      const targetNode = nodes.find(n => {
        if (n.id === tempConnection.sourceId) return false; // Can't connect to self
        if (n.type === 'trigger') return false; // Trigger has no input
        
        // Check if near left side of node
        const dx = worldPos.x - n.x;
        const dy = worldPos.y - (n.y + NODE_HEIGHT/2);
        return Math.abs(dx) < 30 && Math.abs(dy) < 30;
      });

      if (targetNode) {
        setConnections(prev => [
          ...prev, 
          { id: `c-${Date.now()}`, source: tempConnection.sourceId, target: targetNode.id }
        ]);
        setLogs(prev => [{ time: new Date().toLocaleTimeString(), level: 'info', msg: `Connected ${tempConnection.sourceId} to ${targetNode.id}` }, ...prev]);
      }
      setTempConnection(null);
    }
  };

  const handleWheel = (e) => {
    if (e.ctrlKey || e.metaKey) {
      // Zoom
      e.preventDefault();
      const zoomSensitivity = 0.001;
      const newScale = Math.min(Math.max(scale - e.deltaY * zoomSensitivity, 0.2), 3);
      setScale(newScale);
    } else {
      // Pan
      setPan(prev => ({ x: prev.x - e.deltaX, y: prev.y - e.deltaY }));
    }
  };

  const handleAddNode = (type, title) => {
    // Add to center of screen
    const rect = canvasRef.current?.getBoundingClientRect();
    const cx = rect ? (rect.width / 2 - pan.x) / scale : 100;
    const cy = rect ? (rect.height / 2 - pan.y) / scale : 100;

    const newNode = {
      id: `n-${Date.now()}`,
      type,
      title,
      x: cx - NODE_WIDTH/2,
      y: cy - NODE_HEIGHT/2,
      status: 'idle',
      data: { created: 'Just now' }
    };

    setNodes(prev => [...prev, newNode]);
    setSelectedNodeId(newNode.id);
  };

  const handleDeleteNode = (id) => {
    setNodes(prev => prev.filter(n => n.id !== id));
    setConnections(prev => prev.filter(c => c.source !== id && c.target !== id));
    if (selectedNodeId === id) setSelectedNodeId(null);
  };

  const runSimulation = async () => {
    if (isRunning) return;
    setIsRunning(true);
    setLogs(prev => [{ time: new Date().toLocaleTimeString(), level: 'info', msg: 'Starting workflow execution...' }, ...prev]);

    // Reset status
    setNodes(prev => prev.map(n => ({ ...n, status: 'idle' })));

    // Helper to delay
    const wait = (ms) => new Promise(r => setTimeout(r, ms));

    // Simulate flow
    const sequence = [['1'], ['2', '3'], ['4'], ['5'], ['6']];
    
    for (const group of sequence) {
      // Set Running
      setNodes(prev => prev.map(n => group.includes(n.id) ? { ...n, status: 'running' } : n));
      await wait(1500);
      // Set Success
      setNodes(prev => prev.map(n => group.includes(n.id) ? { ...n, status: 'success' } : n));
      
      // Log it
      group.forEach(id => {
         const node = nodes.find(n => n.id === id);
         setLogs(prev => [{ time: new Date().toLocaleTimeString(), level: 'success', msg: `Node executed: ${node?.title}` }, ...prev]);
      });
    }

    setIsRunning(false);
    setLogs(prev => [{ time: new Date().toLocaleTimeString(), level: 'info', msg: 'Workflow completed successfully.' }, ...prev]);
  };

  const selectedNode = nodes.find(n => n.id === selectedNodeId);

  return (
    <div className="flex flex-col h-screen w-screen bg-[#1a1a1a] text-gray-200 font-sans overflow-hidden select-none">
      <TopNav onRun={runSimulation} isRunning={isRunning} />

      <div className="flex-1 flex overflow-hidden">
        
        {/* Left Sidebar */}
        <div className="w-[280px] bg-[#1f1f1f] border-r border-gray-800 flex flex-col z-10 shadow-2xl">
          <div className="p-4 border-b border-gray-800">
            <div className="relative">
              <Search className="absolute left-3 top-2.5 w-4 h-4 text-gray-500" />
              <input 
                type="text" 
                placeholder="Search nodes..." 
                className="w-full bg-[#111] border border-gray-700 rounded-md py-2 pl-9 pr-4 text-sm text-gray-300 focus:outline-none focus:border-indigo-500 transition-colors"
              />
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
            <div className="mb-6">
              <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3 ml-1">Triggers</h3>
              <SidebarItem icon={Zap} label="Webhook" type="trigger" onAdd={handleAddNode} />
              <SidebarItem icon={Activity} label="Cron Schedule" type="trigger" onAdd={handleAddNode} />
              <SidebarItem icon={MousePointer2} label="Manual Click" type="trigger" onAdd={handleAddNode} />
            </div>

            <div className="mb-6">
              <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3 ml-1">Data Sources</h3>
              <SidebarItem icon={Database} label="PostgreSQL" type="source" onAdd={handleAddNode} />
              <SidebarItem icon={Database} label="Redis Cache" type="source" onAdd={handleAddNode} />
              <SidebarItem icon={UploadCloud} label="Rest API" type="source" onAdd={handleAddNode} />
            </div>

            <div className="mb-6">
              <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3 ml-1">Processing</h3>
              <SidebarItem icon={Cpu} label="Javascript Code" type="process" onAdd={handleAddNode} />
              <SidebarItem icon={Activity} label="Filter" type="process" onAdd={handleAddNode} />
              <SidebarItem icon={Database} label="Merge Data" type="process" onAdd={handleAddNode} />
              <SidebarItem icon={Cpu} label="AI Model" type="process" onAdd={handleAddNode} />
            </div>

            <div className="mb-6">
              <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-3 ml-1">Output</h3>
              <SidebarItem icon={Terminal} label="Debug Log" type="output" onAdd={handleAddNode} />
              <SidebarItem icon={UploadCloud} label="HTTP Request" type="output" onAdd={handleAddNode} />
              <SidebarItem icon={Database} label="Write DB" type="output" onAdd={handleAddNode} />
            </div>
          </div>
        </div>

        {/* Main Canvas Area */}
        <div className="flex-1 relative bg-[#121212] overflow-hidden flex flex-col">
          <div 
            ref={canvasRef}
            className="flex-1 relative cursor-grab active:cursor-grabbing overflow-hidden"
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onWheel={handleWheel}
            onMouseLeave={handleMouseUp}
          >
            {/* Grid Background */}
            <div 
              className="absolute inset-0 pointer-events-none opacity-20"
              style={{
                transform: `translate(${pan.x}px, ${pan.y}px) scale(${scale})`,
                transformOrigin: '0 0',
                backgroundImage: `linear-gradient(#333 1px, transparent 1px), linear-gradient(90deg, #333 1px, transparent 1px)`,
                backgroundSize: '40px 40px'
              }}
            />

            {/* Transform Container */}
            <div 
              className="absolute top-0 left-0 w-full h-full origin-top-left"
              style={{ transform: `translate(${pan.x}px, ${pan.y}px) scale(${scale})` }}
            >
              <svg className="absolute top-0 left-0 w-[5000px] h-[5000px] pointer-events-none -z-0 overflow-visible">
                {connections.map(conn => {
                  const source = getNodeCenter(conn.source).out;
                  const target = getNodeCenter(conn.target).in;
                  const sourceNode = nodes.find(n => n.id === conn.source);
                  const isActive = isRunning && sourceNode?.status === 'running';
                  
                  return (
                    <Connection 
                      key={conn.id} 
                      start={source} 
                      end={target} 
                      active={isActive}
                    />
                  );
                })}
                {tempConnection && (
                  <path
                    d={`M ${tempConnection.startX} ${tempConnection.startY} C ${tempConnection.startX + 100} ${tempConnection.startY}, ${tempConnection.endX - 100} ${tempConnection.endY}, ${tempConnection.endX} ${tempConnection.endY}`}
                    fill="none"
                    stroke="#6366f1"
                    strokeWidth="2"
                    strokeDasharray="5,5"
                    opacity="0.6"
                  />
                )}
              </svg>

              {nodes.map(node => (
                <Node 
                  key={node.id} 
                  node={node} 
                  isSelected={selectedNodeId === node.id}
                  onMouseDown={handleNodeMouseDown}
                  onClick={setSelectedNodeId}
                  zoom={scale}
                />
              ))}
            </div>

            {/* Canvas Controls */}
            <div className="absolute bottom-6 right-6 flex flex-col gap-2 bg-[#1f1f1f] p-1.5 rounded-lg border border-gray-700 shadow-xl z-20">
               <button onClick={() => setScale(s => Math.min(s + 0.1, 2))} className="p-2 hover:bg-gray-700 rounded text-gray-400 hover:text-white transition-colors"><ZoomIn className="w-5 h-5"/></button>
               <button onClick={() => setScale(s => Math.max(s - 0.1, 0.2))} className="p-2 hover:bg-gray-700 rounded text-gray-400 hover:text-white transition-colors"><ZoomOut className="w-5 h-5"/></button>
               <div className="h-px bg-gray-700 my-1"></div>
               <button onClick={() => {setPan({x:0,y:0}); setScale(1);}} className="p-2 hover:bg-gray-700 rounded text-xs font-mono text-gray-400 hover:text-white transition-colors">100%</button>
            </div>
          </div>

          {/* Bottom Panel (Logs) */}
          <div className="h-[200px] bg-[#1f1f1f] border-t border-gray-800 flex flex-col z-10">
            <div className="flex items-center border-b border-gray-800">
              <button className="px-4 py-2 text-sm font-medium text-white border-b-2 border-indigo-500 backdrop-blur-sm">
                Execution Logs
              </button>
              <button className="px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-300">
                Data Inspector
              </button>
              <button className="px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-300">
                Errors (0)
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-4 font-mono text-xs custom-scrollbar">
              {logs.map((log, i) => (
                <div key={i} className="flex gap-4 mb-2 opacity-0 animate-in fade-in slide-in-from-bottom-1 fill-mode-forwards" style={{animationDelay: `${i * 50}ms`, animationDuration: '0.3s'}}>
                  <span className="text-gray-500 select-none w-16">{log.time}</span>
                  <span className={`
                    ${log.level === 'info' ? 'text-blue-400' : ''}
                    ${log.level === 'success' ? 'text-emerald-400' : ''}
                    ${log.level === 'error' ? 'text-red-400' : ''}
                    font-semibold w-16 uppercase tracking-wider
                  `}>{log.level}</span>
                  <span className="text-gray-300">{log.msg}</span>
                </div>
              ))}
              {logs.length === 0 && <div className="text-gray-600 italic">Waiting for execution...</div>}
            </div>
          </div>
        </div>

        {/* Right Sidebar (Config) */}
        <div className="w-[320px] bg-[#1f1f1f] border-l border-gray-800 flex flex-col z-10 shadow-2xl transition-all duration-300">
          {selectedNode ? (
            <>
              <div className="p-5 border-b border-gray-800 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${COLORS[selectedNode.type].bg}`} />
                  <span className="font-semibold text-gray-200">{selectedNode.title}</span>
                </div>
                <div className="flex items-center gap-1">
                  <button className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded transition-colors"><MoreVertical className="w-4 h-4"/></button>
                  <button 
                    onClick={() => handleDeleteNode(selectedNode.id)}
                    className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-900/20 rounded transition-colors"
                  >
                    <Trash2 className="w-4 h-4"/>
                  </button>
                </div>
              </div>

              <div className="flex-1 overflow-y-auto p-5 space-y-6 custom-scrollbar">
                
                {/* Node Status */}
                <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-800">
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-2 block">Status</label>
                  <div className="flex items-center gap-2">
                    {selectedNode.status === 'idle' && <span className="w-2 h-2 rounded-full bg-gray-500"></span>}
                    {selectedNode.status === 'running' && <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>}
                    {selectedNode.status === 'success' && <span className="w-2 h-2 rounded-full bg-emerald-500"></span>}
                    <span className="text-sm font-medium text-gray-300 capitalize">{selectedNode.status}</span>
                  </div>
                </div>

                {/* Parameters Form */}
                <div className="space-y-4">
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-widest">Parameters</label>
                  
                  <div>
                    <label className="block text-xs text-gray-400 mb-1">Node Name</label>
                    <input 
                      value={selectedNode.title} 
                      onChange={(e) => setNodes(prev => prev.map(n => n.id === selectedNode.id ? {...n, title: e.target.value} : n))}
                      className="w-full bg-[#111] border border-gray-700 rounded p-2 text-sm text-gray-200 focus:border-indigo-500 focus:outline-none transition-colors"
                    />
                  </div>

                  {Object.entries(selectedNode.data).map(([key, value]) => (
                     <div key={key}>
                     <label className="block text-xs text-gray-400 mb-1 capitalize">{key}</label>
                     <input 
                       value={value} 
                       onChange={(e) => {
                         const newData = {...selectedNode.data, [key]: e.target.value};
                         setNodes(prev => prev.map(n => n.id === selectedNode.id ? {...n, data: newData} : n));
                       }}
                       className="w-full bg-[#111] border border-gray-700 rounded p-2 text-sm text-gray-200 focus:border-indigo-500 focus:outline-none transition-colors font-mono"
                     />
                   </div>
                  ))}

                  <button className="flex items-center gap-2 text-xs text-indigo-400 hover:text-indigo-300 mt-2 font-medium transition-colors">
                    <Plus className="w-3 h-3" /> Add Parameter
                  </button>
                </div>

                {/* Documentation / Info */}
                <div className="space-y-2 pt-4 border-t border-gray-800">
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-widest">Info</label>
                  <p className="text-xs text-gray-400 leading-relaxed">
                    This node processes incoming data streams using the configured logic. Ensure input schema matches expected format JSON.
                  </p>
                </div>

              </div>
              
              <div className="p-4 border-t border-gray-800 bg-gray-900/30">
                <button className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-sm font-medium transition-colors shadow-lg shadow-indigo-900/20">
                  Apply Changes
                </button>
              </div>
            </>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-8 opacity-50">
              <MousePointer2 className="w-12 h-12 text-gray-600 mb-4" />
              <h3 className="text-gray-300 font-medium mb-1">No Node Selected</h3>
              <p className="text-xs text-gray-500 max-w-[200px]">Click on a node in the canvas to view and edit its properties.</p>
            </div>
          )}
        </div>

      </div>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
          height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #1a1a1a;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #333;
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #444;
        }
      `}</style>
    </div>
  );
}