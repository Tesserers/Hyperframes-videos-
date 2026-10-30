import React, { createContext, useContext } from 'react';
import { useCurrentFrame } from 'remotion';

/**
 * Ritmo global de una pieza. pace = 1 es el timing de diseño; 0.85 la
 * alarga un 18 %, 1.2 la acelera. Todas las primitivas leen el frame a
 * través de useFrame(), así la coreografía se estira entera sin romperse.
 */
const PaceContext = createContext(1);

export const PaceProvider: React.FC<{ pace: number; children: React.ReactNode }> = ({ pace, children }) => (
  <PaceContext.Provider value={pace}>{children}</PaceContext.Provider>
);

export const useFrame = () => useCurrentFrame() * useContext(PaceContext);
