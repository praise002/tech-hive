'use client';

import {
  LiveblocksProvider,
  RoomProvider,
  ClientSideSuspense,
} from '@liveblocks/react/suspense';

import { publicApiKey } from '../../utils/liveblock';
import TextEditor from './TextEditor';
import Spinner from '../../components/common/Spinner';

function Liveblock() {
  return (
    <LiveblocksProvider publicApiKey={publicApiKey}>
      <RoomProvider id="my-room">
        <ClientSideSuspense
          fallback={
            <div className="py-50 px-4 sm:px-6 lg:px-8 bg-white dark:bg-dark">
              <Spinner />
            </div>
          }
        >
          <TextEditor />
        </ClientSideSuspense>
      </RoomProvider>
    </LiveblocksProvider>
  );
}

export default Liveblock;
