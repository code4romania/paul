import { FlashMessage } from '@/types/FlashMessage';
import { omit } from 'lodash';
import { create } from 'zustand';

type Alert = 'success' | 'error';

type NotifyState = {
  alert?: Alert;
  message?: string | FlashMessage[];
  show: boolean;

  actions: {
    clearNotification: () => void;
    hideNotification: () => void;
    notifyError: (message: string | FlashMessage[]) => void;
    notifySuccess: (message: string | FlashMessage[]) => void;
    notify: (message: string | FlashMessage[], alert?: Alert) => void;
  };
};

const useNotifyStore = create<NotifyState>((set) => ({
  alert: 'success',
  message: 'Success',
  show: false,

  actions: {
    clearNotification: () =>
      set((state) => omit(state, ['alert', 'message']), true),
    hideNotification: () => set({ show: false }),
    notifyError: (message) =>
      set(() => ({ alert: 'error', message, show: true })),
    notifySuccess: (message) =>
      set(() => ({ alert: 'success', message, show: true })),
    notify: (message, alert) => set(() => ({ alert, message, show: true })),
  },
}));

export const useNotifyAlert = () => useNotifyStore((s) => s.alert);
export const useNotifyMessage = () => useNotifyStore((s) => s.message);
export const useNotifyShow = () => useNotifyStore((s) => s.show);

export const useNotifyActions = () => useNotifyStore((s) => s.actions);
