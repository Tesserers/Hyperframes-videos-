import React from 'react';
import { Composition } from 'remotion';
import { brand } from './brand/linkeddy.config';
import { loadBrandFonts } from './brand/fonts';
import { pieces } from './compositions/registry';

loadBrandFonts();

export const RemotionRoot: React.FC = () => (
  <>
    {pieces.map((piece) => (
      <Composition
        key={piece.id}
        id={piece.id}
        component={piece.component}
        schema={piece.schema}
        defaultProps={piece.defaultProps}
        durationInFrames={piece.duration(piece.defaultProps)}
        calculateMetadata={({ props }: { props: Record<string, unknown> }) => ({ durationInFrames: piece.duration(props) })}
        width={brand.video.width}
        height={brand.video.height}
        fps={brand.video.fps}
      />
    ))}
  </>
);
