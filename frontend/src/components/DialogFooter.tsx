import { MouseEventHandler } from 'react';
import { Button } from './Button';

type DialogFooterProps = {
  disabled?: boolean;
  mainButton: {
    disabled?: boolean;
    label: string;
    onClick: MouseEventHandler;
  };
  secondaryButton?: {
    disabled?: boolean;
    label: string;
    onClick: MouseEventHandler;
  };
};

export function DialogFooter({
  disabled,
  mainButton,
  secondaryButton,
}: DialogFooterProps) {
  return (
    <div className='flex justify-end items-center gap-x-6 bg-[#F8F6F2] rounded-b-xl p-6'>
      {secondaryButton && (
        <Button
          disabled={disabled || secondaryButton.disabled}
          onClick={secondaryButton.onClick}
          variant='outlined'
          type='button'
        >
          {secondaryButton.label}
        </Button>
      )}
      <Button
        disabled={disabled || mainButton.disabled}
        onClick={mainButton.onClick}
      >
        {mainButton.label}
      </Button>
    </div>
  );
}
