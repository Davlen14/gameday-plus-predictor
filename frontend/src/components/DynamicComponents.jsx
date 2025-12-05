import React from 'react';
import { CONFIG } from '../config.js';

// Dynamic Glass Card Component
export const GlassCard = ({ 
    title, 
    children, 
    className = '', 
    icon = null, 
    comingSoon = false,
    strong = false 
}) => {
    const cardClass = strong ? 'glass-card-strong' : 'glass-card';
    const opacity = comingSoon ? 'opacity-60' : 'opacity-100';
    
    return (
        <div className={`relative overflow-hidden rounded-2xl ${cardClass} p-6 ${className} ${opacity} section-ready fade-in`}>
            <div className="card-shine"></div>
            <div className="relative z-10">
                <div className="flex items-center gap-2 mb-4">
                    {icon && <div className="text-white">{icon}</div>}
                    <h3 className="text-white font-semibold text-lg">{title}</h3>
                </div>
                {comingSoon ? (
                    <ComingSoonContent title={title} />
                ) : (
                    children
                )}
            </div>
        </div>
    );
};

// Dynamic Prediction Card Component
export const PredictionCard = ({ 
    label, 
    value, 
    detail, 
    type = 'neutral',
    size = 'normal',
    onClick = null 
}) => {
    const colors = {
        positive: 'from-emerald-500/20 to-green-500/20 border-emerald-500/40',
        negative: 'from-red-500/20 to-rose-500/20 border-red-500/40',
        warning: 'from-amber-500/20 to-yellow-500/20 border-amber-500/40',
        neutral: 'from-cyan-500/20 to-blue-500/20 border-cyan-500/40'
    };

    const textSize = size === 'large' ? 'text-6xl' : 'text-5xl';
    const cardClass = onClick ? 'cursor-pointer transform hover:scale-105' : '';
    
    return (
        <div className={`relative group ${cardClass}`} onClick={onClick}>
            <div className={`absolute -inset-0.5 bg-gradient-to-br ${colors[type]} rounded-lg blur-xl opacity-50 group-hover:opacity-75 transition duration-300`}></div>
            <div className={`relative overflow-hidden rounded-lg glass-card p-6 border ${colors[type].split(' ')[2]} shadow-xl slide-up`}>
                <div className="card-shine"></div>
                <div className="relative z-10 space-y-3">
                    <h3 className="text-slate-300 text-sm font-medium">{label}</h3>
                    <div className={`metric-value-${type}`}>
                        <span className={`${textSize} analytical-number font-bold`}>{value}</span>
                    </div>
                    <p className="text-slate-400 text-sm analytical-number">{detail}</p>
                </div>
            </div>
        </div>
    );
};

// Dynamic Data Table Component
export const DataTable = ({ headers, rows, className = '' }) => {
    return (
        <div className="overflow-x-auto">
            <table className={`w-full border-collapse rounded-xl overflow-hidden glass-card ${className}`}>
                <thead>
                    <tr>
                        {headers.map((header, index) => (
                            <th 
                                key={index} 
                                className="border border-slate-600 p-3 text-left text-slate-300 font-bold text-sm backdrop-blur-sm"
                            >
                                {header}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {rows.map((row, rowIndex) => (
                        <tr key={rowIndex} className="hover:bg-slate-700/30 transition-colors">
                            {row.map((cell, cellIndex) => (
                                <td 
                                    key={cellIndex} 
                                    className="border border-slate-600 p-3 analytical-number"
                                >
                                    {cell}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

// Dynamic Team Logo Component
export const TeamLogo = ({ team, size = 'md', className = '' }) => {
    const sizes = {
        sm: 'w-8 h-8',
        md: 'w-12 h-12',
        lg: 'w-16 h-16',
        xl: 'w-20 h-20'
    };

    if (!team) return null;

    return (
        <div className={`${sizes[size]} ${className} flex items-center justify-center`}>
            <img 
                src={team.logo || team.logos?.[0]} 
                alt={`${team.school || team.name} logo`}
                className="w-full h-full object-contain"
                onError={(e) => {
                    e.target.src = `https://via.placeholder.com/100x100?text=${(team.school || team.name).charAt(0)}`;
                }}
            />
        </div>
    );
};

// Dynamic Loading Spinner
export const LoadingSpinner = ({ size = 'md', className = '' }) => {
    const sizes = {
        sm: 'w-4 h-4',
        md: 'w-8 h-8',
        lg: 'w-12 h-12',
        xl: 'w-16 h-16'
    };

    return (
        <div className={`${sizes[size]} ${className} animate-spin`}>
            <div className="w-full h-full border-4 border-slate-600 border-t-cyan-500 rounded-full"></div>
        </div>
    );
};

// Dynamic Error Display
export const ErrorDisplay = ({ error, onRetry, className = '' }) => {
    return (
        <div className={`glass-card p-6 border border-red-500/40 ${className}`}>
            <div className="text-center space-y-4">
                <div className="text-red-400 text-lg font-semibold">⚠️ Error</div>
                <p className="text-slate-300">{error}</p>
                {onRetry && (
                    <button 
                        onClick={onRetry}
                        className="px-4 py-2 bg-red-500/20 border border-red-500/40 rounded-lg text-white hover:bg-red-500/30 transition-colors"
                    >
                        Try Again
                    </button>
                )}
            </div>
        </div>
    );
};

// Dynamic Coming Soon Component
export const ComingSoonContent = ({ title }) => {
    return (
        <div className="text-center py-8">
            <div className="text-slate-400 text-2xl font-bold mb-2">🚧 Coming Soon</div>
            <p className="text-slate-500">Advanced {title.toLowerCase()} functionality is being developed</p>
            <div className="mt-4 text-sm text-slate-600">
                This feature will include real-time data and advanced analytics
            </div>
        </div>
    );
};

// Dynamic Section Container
export const SectionContainer = ({ children, className = '' }) => {
    return (
        <div className={`space-y-6 ${className}`}>
            {children}
        </div>
    );
};

// Dynamic Metric Display
export const MetricDisplay = ({ 
    label, 
    value, 
    comparison = null, 
    type = 'neutral',
    format = 'number',
    className = ''
}) => {
    const formatValue = (val) => {
        switch (format) {
            case 'percentage':
                return `${val}%`;
            case 'currency':
                return `$${val}`;
            case 'decimal':
                return Number(val).toFixed(3);
            default:
                return val;
        }
    };

    return (
        <div className={`space-y-1 ${className}`}>
            <div className="text-slate-400 text-sm font-medium">{label}</div>
            <div className={`metric-value-${type} text-2xl font-bold analytical-number`}>
                {formatValue(value)}
            </div>
            {comparison && (
                <div className="text-xs text-slate-500">
                    vs {formatValue(comparison)}
                </div>
            )}
        </div>
    );
};