import { XMarkIcon } from '@heroicons/react/20/solid';

type DialogTitleProps = {
  onClose: () => void;
  title: string;
};

export function DialogTitle({ onClose, title }: DialogTitleProps) {
  return (
    <div className='flex justify-between items-center p-6'>
      <h3 className='font-amalia-bold text-2xl text-black'>{title}</h3>
      <button
        className='h-full w-8 flex shrink-0 items-center'
        onClick={onClose}
      >
        <XMarkIcon />
      </button>
    </div>
  );
}
