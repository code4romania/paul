import { Transition } from '@headlessui/react';
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline';
import { Fragment } from 'react';
import {
  useNotifyActions,
  useNotifyAlert,
  useNotifyMessage,
  useNotifyShow,
} from '@/stores/useNotifyStore';

export function Notification() {
  const alert = useNotifyAlert();
  const message = useNotifyMessage();
  const show = useNotifyShow();
  const { clearNotification, hideNotification } = useNotifyActions();

  const autoHide = () => {
    setTimeout(hideNotification, 15000);
  };

  return (
    <Transition
      afterEnter={autoHide}
      afterLeave={clearNotification}
      as={Fragment}
      show={show}
      enter='transition ease-in-out duration-300 transform'
      enterFrom='-translate-y-full'
      enterTo='translate-y-0'
      leave='transition ease-in-out duration-300 transform'
      leaveFrom='translate-y-0'
      leaveTo='-translate-y-full'
    >
      <div className='flex rounded-md shadow-md items-center p-4 gap-3 absolute top-3 right-3 min-w-[300px] max-w-xl z-50 bg-white'>
        {alert === 'success' && (
          <CheckCircleIcon className='h-5 text-[#34D399]' />
        )}
        {alert === 'error' && <ExclamationTriangleIcon className='h-5' />}
        {typeof message === 'string'
          ? message
          : message?.map((flashMessage) => (
              <div key={flashMessage.message}>{flashMessage.message}</div>
            ))}
        <button
          className='h-full w-5 flex shrink-0 items-center ml-auto'
          onClick={hideNotification}
        >
          <XMarkIcon />
        </button>
      </div>
    </Transition>
  );
}
