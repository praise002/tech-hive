'use client';

import {
  LiveblocksProvider,
  RoomProvider,
  ClientSideSuspense,
} from '@liveblocks/react/suspense';

import { publicApiKey } from '../../utils/liveblock';
import { Editor } from './Editor';

function Liveblock() {
  return (
    <LiveblocksProvider publicApiKey={publicApiKey}>
      <RoomProvider id="my-room">
        <ClientSideSuspense fallback={<div className='mt-50 bg-white'>Loading…</div>}>
          <Editor />
        </ClientSideSuspense>
      </RoomProvider>
    </LiveblocksProvider>
  );
}

export default Liveblock;
